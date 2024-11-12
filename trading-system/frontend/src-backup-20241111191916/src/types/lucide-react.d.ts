declare module 'lucide-react' {
    import { ComponentType } from 'react';

    interface IconProps extends React.SVGProps<SVGSVGElement> {
        size?: number | string;
        color?: string;
        strokeWidth?: number;
    }

    export const ArrowUpCircle: ComponentType<IconProps>;
    export const ArrowDownCircle: ComponentType<IconProps>;
    export const Target: ComponentType<IconProps>;
    export const AlertTriangle: ComponentType<IconProps>;
    export const TrendingUp: ComponentType<IconProps>;
    export const BarChart2: ComponentType<IconProps>;
    export const Activity: ComponentType<IconProps>;
}
