declare module 'lucide-react' {
    import { FC, SVGProps } from 'react'
    
    interface IconProps extends SVGProps<SVGSVGElement> {
      size?: string | number
      color?: string
      strokeWidth?: string | number
    }
  
    export type Icon = FC<IconProps>
  
    export const ArrowUpCircle: Icon
    export const ArrowDownCircle: Icon
    export const Target: Icon
    export const AlertTriangle: Icon
    export const TrendingUp: Icon
    export const BarChart2: Icon
    export const Activity: Icon
  }