import type { User } from './user'

export interface Comment {
  id: string
  photo_id: string
  user_id: string
  user: User
  content: string
  is_deleted: boolean
  created_at: string
  updated_at: string
}

export interface CommentList {
  comments: Comment[]
  total: number
}

export interface CreateCommentRequest {
  content: string
}

export interface UpdateCommentRequest {
  content: string
}
