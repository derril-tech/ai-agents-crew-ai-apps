export interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
}

export interface ChatRequest {
  message: string
  history: Message[]
  conversationId?: string
}

export interface ChatResponse {
  response: string
  conversationId: string
  sources?: string[]
}

export interface Conversation {
  id: string
  title: string
  messages: Message[]
  createdAt: string
  updatedAt: string
}
