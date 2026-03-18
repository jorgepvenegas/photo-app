export interface User {
  id: string
  email: string
  is_active: boolean
  is_verified: boolean
  created_at: string
}

export interface UserProfile extends User {
  photos_count: number
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
}
