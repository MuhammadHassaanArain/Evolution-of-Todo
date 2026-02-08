// Mock auth client implementation to avoid build errors
export const authClient = {
  useAuth: () => ({ user: null, isLoading: false, isAuthenticated: false }),
  signIn: async () => {},
  signOut: async () => {},
};

// Export auth hooks for use in components
export const { useAuth, signIn, signOut } = authClient;