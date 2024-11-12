// src/components/common/LazyLoad.tsx
import React, { Suspense } from 'react';

interface Props {
  component: React.LazyExoticComponent<any>;
  fallback?: React.ReactNode;
}

export const LazyLoad: React.FC<Props> = ({ 
  component: Component,
  fallback = <div>Loading...</div>
}) => (
  <Suspense fallback={fallback}>
    <Component />
  </Suspense>
);

