export interface Photo {
  id: string
  user_id: string
  title: string
  description: string | null
  storage_url: string
  thumb_small_url: string | null
  thumb_medium_url: string | null
  thumb_large_url: string | null
  width: number
  height: number
  file_size: number
  is_public: boolean
  created_at: string
  updated_at: string
}

export interface PhotoDetail extends Photo {
  user: {
    id: string
    email: string
  }
  comments_count: number
}

export interface PhotoList {
  photos: Photo[]
  total: number
  page: number
  per_page: number
}

export interface UploadRequest {
  filename: string
  content_type: string
  file_size: number
}

export interface PresignedUrlResponse {
  upload_url: string
  fields?: Record<string, string>
  storage_key: string
  expires_in: number
}

export interface UploadConfirmRequest {
  storage_key: string
  title: string
  description: string | null
  width: number
  height: number
  file_size: number
  mime_type: string
  is_public: boolean
}
