"use client"

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Send, Bot, User, Loader2 } from 'lucide-react'
import { useChat } from '@/hooks/use-chat'
import { Message } from '@/types/chat'

interface ChatInterfaceProps {
  initialMessages?: Message[]
  apiEndpoint?: string
}

export function ChatInterface({ initialMessages = [], apiEndpoint = '/api/chat' }: ChatInterfaceProps) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const { messages, isLoading, sendMessage, error } = useChat({
    apiEndpoint,
    initialMessages
  })

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return
    
    await sendMessage(input)
    setInput('')
  }

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <CardHeader className="border-b">
        <CardTitle className="flex items-center gap-2">
          <Bot className="w-6 h-6 text-blue-500" />
          AI Chatbot
        </CardTitle>
      </CardHeader>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 dark:bg-gray-800'
              }`}
            >
              <div className="flex items-start gap-2">
                {message.role === 'assistant' && (
                  <Bot className="w-4 h-4 mt-1 text-blue-500 flex-shrink-0" />
                )}
                {message.role === 'user' && (
                  <User className="w-4 h-4 mt-1 text-white flex-shrink-0" />
                )}
                <div className="flex-1">
                  <p className="text-sm">{message.content}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <Bot className="w-4 h-4 text-blue-500" />
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <Card className="border-t-0 rounded-t-none">
        <CardContent className="p-4">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading || !input.trim()}>
              <Send className="w-4 h-4" />
            </Button>
          </form>
          
          {error && (
            <p className="text-red-500 text-sm mt-2">{error}</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
