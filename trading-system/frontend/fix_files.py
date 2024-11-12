import os
import re
from typing import List, Dict, Optional
import logging
from pathlib import Path

class TypeScriptFixer:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.setup_logging()
        
        # Type definitions that need to be added
        self.missing_types = {
            'TechnicalIndicator': '''
export interface TechnicalIndicator {
    name: string;
    value: number;
    signal: 'BUY' | 'SELL' | 'NEUTRAL';
    timeframe: string;
    metadata?: Record<string, any>;
}''',
            'MLAnalysis': '''
export interface MLAnalysis {
    prediction: 'BUY' | 'SELL' | 'NEUTRAL';
    confidence: number;
    patternRecognition: {
        pattern: string;
        probability: number;
    }[];
    supportingFactors?: string[];
}''',
            'PerformanceMetrics': '''
export interface PerformanceMetrics {
    winRate: {
        overall: number;
        byTimeframe: Record<string, number>;
    };
    profitLoss: {
        total: number;
        byStrategy: Record<string, number>;
    };
    riskAdjustedReturns: {
        sharpeRatio: number;
        sortinoRatio: number;
        calmarRatio: number;
    };
    drawdown: {
        current: number;
        maximum: number;
        average: number;
        duration: number;
    };
}'''
        }

        # Import fixes
        self.import_fixes = {
            'PerformanceTrackingPanel.tsx': [
                "import { PerformanceMetrics } from '../types/market';",
                "import { Card } from '../common/Card';",
                "import { formatPercentage, formatNumber } from '../utils/formatters';"
            ],
            'TradingAnalysisService.ts': [
                "import { MarketSignal, MarketConditions, TimeframeData } from '../types/market';",
                "import { RiskMetrics, MarketScan } from '../types/trading';"
            ]
        }

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('typescript_fixer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def scan_for_errors(self) -> List[Dict]:
        """Scan TypeScript files for common errors"""
        errors = []
        for file_path in self.root_dir.rglob('*.ts*'):
            try:
                content = file_path.read_text()
                file_errors = self.analyze_file(content, file_path)
                if file_errors:
                    errors.extend(file_errors)
            except Exception as e:
                self.logger.error(f"Error scanning {file_path}: {str(e)}")
        return errors

    def analyze_file(self, content: str, file_path: Path) -> List[Dict]:
        """Analyze a single file for errors"""
        errors = []
        
        # Check for missing imports
        missing_imports = self.check_missing_imports(content)
        if missing_imports:
            errors.append({
                'file': str(file_path),
                'type': 'missing_import',
                'details': missing_imports
            })

        # Check for missing type definitions
        missing_types = self.check_missing_types(content)
        if missing_types:
            errors.append({
                'file': str(file_path),
                'type': 'missing_type',
                'details': missing_types
            })

        # Check for any usage
        any_usages = self.check_any_usage(content)
        if any_usages:
            errors.append({
                'file': str(file_path),
                'type': 'any_usage',
                'details': any_usages
            })

        return errors

    def fix_errors(self, errors: List[Dict]):
        """Fix detected errors"""
        for error in errors:
            try:
                file_path = Path(error['file'])
                content = file_path.read_text()
                
                if error['type'] == 'missing_import':
                    content = self.fix_imports(content, error['details'])
                elif error['type'] == 'missing_type':
                    content = self.fix_types(content, error['details'])
                elif error['type'] == 'any_usage':
                    content = self.fix_any_usage(content, error['details'])
                
                # Create backup
                backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                file_path.rename(backup_path)
                
                # Write fixed content
                file_path.write_text(content)
                self.logger.info(f"Fixed {error['type']} in {file_path}")
                
            except Exception as e:
                self.logger.error(f"Error fixing {error['file']}: {str(e)}")

    def fix_imports(self, content: str, missing_imports: List[str]) -> str:
        """Fix missing imports"""
        import_block = '\n'.join(missing_imports)
        if 'import' in content:
            # Add after last import
            pattern = r'^import.*?$\n'
            matches = list(re.finditer(pattern, content, re.MULTILINE))
            if matches:
                last_import = matches[-1]
                return content[:last_import.end()] + import_block + '\n' + content[last_import.end():]
        return import_block + '\n' + content

    def fix_types(self, content: str, missing_types: List[str]) -> str:
        """Fix missing type definitions"""
        types_block = '\n'.join(self.missing_types[t] for t in missing_types)
        # Add types after imports
        import_end = self.find_import_block_end(content)
        return content[:import_end] + '\n' + types_block + content[import_end:]

    def fix_any_usage(self, content: str, any_usages: List[Dict]) -> str:
        """Fix 'any' type usage"""
        for usage in reversed(any_usages):  # Process in reverse to maintain positions
            line_start = content.rfind('\n', 0, usage['position']) + 1
            line_end = content.find('\n', usage['position'])
            if line_end == -1:
                line_end = len(content)
            
            line = content[line_start:line_end]
            fixed_line = line.replace(': any', f": {usage['suggested_type']}")
            content = content[:line_start] + fixed_line + content[line_end:]
        
        return content

    @staticmethod
    def find_import_block_end(content: str) -> int:
        """Find the end of the import block"""
        import_pattern = r'^import.*?$\n'
        matches = list(re.finditer(import_pattern, content, re.MULTILINE))
        if matches:
            return matches[-1].end()
        return 0

    def check_missing_imports(self, content: str) -> List[str]:
        """Check for missing imports"""
        missing = []
        for file_type, imports in self.import_fixes.items():
            if any(imp.split(' ')[-1].rstrip(';') in content for imp in imports):
                missing.extend(imports)
        return list(set(missing))

    def check_missing_types(self, content: str) -> List[str]:
        """Check for missing type definitions"""
        return [type_name for type_name in self.missing_types.keys()
                if type_name in content and f"interface {type_name}" not in content]

    def check_any_usage(self, content: str) -> List[Dict]:
        """Check for 'any' type usage"""
        any_usages = []
        pattern = r': any\b'
        for match in re.finditer(pattern, content):
            # Try to suggest a more specific type
            suggested_type = self.suggest_type(content, match.start())
            any_usages.append({
                'position': match.start(),
                'suggested_type': suggested_type
            })
        return any_usages

    def suggest_type(self, content: str, position: int) -> str:
        """Suggest a more specific type based on context"""
        # Simple type suggestion logic - could be enhanced
        line_start = content.rfind('\n', 0, position) + 1
        line = content[line_start:position]
        
        if 'number' in line.lower():
            return 'number'
        elif 'string' in line.lower():
            return 'string'
        elif 'boolean' in line.lower():
            return 'boolean'
        elif 'array' in line.lower():
            return 'unknown[]'
        
        return 'unknown'

if __name__ == "__main__":
    fixer = TypeScriptFixer("./frontend/src")
    errors = fixer.scan_for_errors()
    if errors:
        print(f"Found {len(errors)} issues to fix")
        fixer.fix_errors(errors)
        print("Fixes applied. Check typescript_fixer.log for details")
    else:
        print("No issues found")