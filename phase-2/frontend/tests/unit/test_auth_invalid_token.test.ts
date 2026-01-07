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

import { isAuthenticated, isTokenExpiringSoon, getTimeUntilExpiration } from '../../src/services/auth';

describe('Invalid token handling', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  test('isAuthenticated returns false when token is malformed', () => {
    // Malformed token with invalid base64 encoding
    const malformedToken = 'invalid.token.format';
    (localStorageMock.getItem as jest.Mock).mockReturnValue(malformedToken);

    const result = isAuthenticated();

    expect(result).toBe(false);
  });

  test('isAuthenticated returns false when token has invalid payload', () => {
    // Token with invalid JSON in payload
    const invalidPayloadToken = 'header.invalid_json_payload.signature';
    (localStorageMock.getItem as jest.Mock).mockReturnValue(invalidPayloadToken);

    const result = isAuthenticated();

    expect(result).toBe(false);
  });

  test('isTokenExpiringSoon returns true when token is malformed', () => {
    // Malformed token with invalid base64 encoding
    const malformedToken = 'invalid.token.format';
    (localStorageMock.getItem as jest.Mock).mockReturnValue(malformedToken);

    const result = isTokenExpiringSoon();

    // According to our implementation, if we can't parse, it assumes the token is expiring
    expect(result).toBe(true);
  });

  test('getTimeUntilExpiration returns null when token is malformed', () => {
    // Malformed token with invalid base64 encoding
    const malformedToken = 'invalid.token.format';
    (localStorageMock.getItem as jest.Mock).mockReturnValue(malformedToken);

    const result = getTimeUntilExpiration();

    expect(result).toBeNull();
  });

  test('isAuthenticated returns false when token has no expiration claim', () => {
    // Token payload without expiration claim
    const payload = { sub: 'test_user' }; // No exp field
    const encodedPayload = Buffer.from(JSON.stringify(payload)).toString('base64');
    const noExpToken = `header.${encodedPayload}.signature`;
    (localStorageMock.getItem as jest.Mock).mockReturnValue(noExpToken);

    const result = isAuthenticated();

    // This would fail when trying to access payload.exp, causing the function to return false
    expect(result).toBe(false);
  });
});