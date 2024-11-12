// src/contexts/AppContext.tsx
import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface State {
  user: any | null;
  theme: 'light' | 'dark';
}

type Action = 
  | { type: 'SET_USER'; payload: any }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' };

const initialState: State = {
  user: null,
  theme: 'light'
};

const AppContext = createContext<{
  state: State;
  dispatch: React.Dispatch<Action>;
}>({ state: initialState, dispatch: () => null });

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer((state: State, action: Action) => {
    switch (action.type) {
      case 'SET_USER':
        return { ...state, user: action.payload };
      case 'SET_THEME':
        return { ...state, theme: action.payload };
      default:
        return state;
    }
  }, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export const useApp = () => useContext(AppContext);

