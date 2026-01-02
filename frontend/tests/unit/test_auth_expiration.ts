// Mock localStorage for testing
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

// Mock window object
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Import the functions to test
import { isAuthenticated, isTokenExpiringSoon, getTimeUntilExpiration } from '../../src/services/auth';

describe('Token expiration handling', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  test('isAuthenticated returns false when no token exists', () => {
    (localStorageMock.getItem as jest.Mock).mockReturnValue(null);

    const result = isAuthenticated();

    expect(result).toBe(false);
    expect(localStorageMock.getItem).toHaveBeenCalledWith('access_token');
  });

  test('isAuthenticated returns false when token is expired', () => {
    // Create a token with an expired time (past date)
    const expiredToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjEyMzQ1Njc4OTB9.dummy_signature'; // exp: 1234567890 (past date)
    (localStorageMock.getItem as jest.Mock).mockReturnValue(expiredToken);

    const result = isAuthenticated();

    expect(result).toBe(false);
  });

  test('isAuthenticated returns true when token is valid and not expired', () => {
    // Create a token with a future expiration time
    const futureTime = Math.floor(Date.now() / 1000) + 3600; // 1 hour from now
    const payload = { sub: 'test_user', exp: futureTime };
    const encodedPayload = Buffer.from(JSON.stringify(payload)).toString('base64');
    const validToken = `header.${encodedPayload}.signature`;
    (localStorageMock.getItem as jest.Mock).mockReturnValue(validToken);

    const result = isAuthenticated();

    expect(result).toBe(true);
  });

  test('isTokenExpiringSoon returns true when token expires soon', () => {
    // Create a token that expires in 3 minutes (less than 5 minutes)
    const soonTime = Math.floor(Date.now() / 1000) + 180; // 3 minutes from now
    const payload = { sub: 'test_user', exp: soonTime };
    const encodedPayload = Buffer.from(JSON.stringify(payload)).toString('base64');
    const expiringSoonToken = `header.${encodedPayload}.signature`;
    (localStorageMock.getItem as jest.Mock).mockReturnValue(expiringSoonToken);

    const result = isTokenExpiringSoon();

    expect(result).toBe(true);
  });

  test('isTokenExpiringSoon returns false when token does not expire soon', () => {
    // Create a token that expires in 10 minutes (more than 5 minutes)
    const futureTime = Math.floor(Date.now() / 1000) + 600; // 10 minutes from now
    const payload = { sub: 'test_user', exp: futureTime };
    const encodedPayload = Buffer.from(JSON.stringify(payload)).toString('base64');
    const validToken = `header.${encodedPayload}.signature`;
    (localStorageMock.getItem as jest.Mock).mockReturnValue(validToken);

    const result = isTokenExpiringSoon();

    expect(result).toBe(false);
  });

  test('getTimeUntilExpiration returns correct time remaining', () => {
    // Create a token that expires in 5 minutes
    const futureTime = Math.floor(Date.now() / 1000) + 300; // 5 minutes from now
    const payload = { sub: 'test_user', exp: futureTime };
    const encodedPayload = Buffer.from(JSON.stringify(payload)).toString('base64');
    const validToken = `header.${encodedPayload}.signature`;
    (localStorageMock.getItem as jest.Mock).mockReturnValue(validToken);

    const result = getTimeUntilExpiration();

    // Should be approximately 300 seconds (5 minutes)
    expect(result).toBeGreaterThanOrEqual(295); // Allow for small timing differences
    expect(result).toBeLessThanOrEqual(305);
  });

  test('getTimeUntilExpiration returns null when no token exists', () => {
    (localStorageMock.getItem as jest.Mock).mockReturnValue(null);

    const result = getTimeUntilExpiration();

    expect(result).toBeNull();
  });

  test('getTimeUntilExpiration returns 0 when token is already expired', () => {
    // Create a token with an expired time (past date)
    const expiredTime = Math.floor(Date.now() / 1000) - 300; // 5 minutes ago
    const payload = { sub: 'test_user', exp: expiredTime };
    const encodedPayload = Buffer.from(JSON.stringify(payload)).toString('base64');
    const expiredToken = `header.${encodedPayload}.signature`;
    (localStorageMock.getItem as jest.Mock).mockReturnValue(expiredToken);

    const result = getTimeUntilExpiration();

    expect(result).toBe(0);
  });
});