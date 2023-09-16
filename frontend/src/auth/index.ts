import jwt_decode from 'jwt-decode';

export function hasPermission(permission: string, token: string): boolean {
  const payload = jwt_decode(token) as any;
  return (
    payload &&
    payload.permissions &&
    payload.permissions.length &&
    payload.permissions.includes(permission)
  );
}
