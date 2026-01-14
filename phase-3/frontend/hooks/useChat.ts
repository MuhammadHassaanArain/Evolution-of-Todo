'use client';
import { useState, useEffect } from 'react';

interface Message {
  id: number;
  role: string;
  content: string;
  createdAt: string;
}

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);

  // Load messages for a conversation if conversationId is set
  useEffect(() => {
    if (conversationId) {
      loadConversationMessages(conversationId);
    } else {
      // Show initial welcome message for new conversations
      setMessages([
        {
          id: 1,
          role: 'assistant',
          content: 'Hello! I\'m your todo assistant. How can I help you today?',
          createdAt: new Date().toISOString(),
        }
      ]);
    }
  }, [conversationId]);

  const loadConversationMessages = async (id: number) => {
    try {
      const response = await fetch(`/api/conversations/${id}/messages`);
      if (response.ok) {
        const data = await response.json();
        // Transform API response to match our Message interface
        const transformedMessages: Message[] = data.map((msg: any) => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
          createdAt: msg.created_at
        }));
        setMessages(transformedMessages);
      } else {
        console.error('Failed to load conversation messages');
        // Show initial welcome message
        setMessages([
          {
            id: 1,
            role: 'assistant',
            content: 'Hello! I\'m your todo assistant. How can I help you today?',
            createdAt: new Date().toISOString(),
          }
        ]);
      }
    } catch (error) {
      console.error('Error loading conversation messages:', error);
      // Show initial welcome message
      setMessages([
        {
          id: 1,
          role: 'assistant',
          content: 'Hello! I\'m your todo assistant. How can I help you today?',
          createdAt: new Date().toISOString(),
        }
      ]);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message to the list
    const userMessage: Message = {
      id: Date.now(), // Use timestamp for unique ID until we get server response
      role: 'user',
      content: input,
      createdAt: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    const messageToSend = input;
    setInput('');

    try {
      // Call the chat API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: messageToSend,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json();

      // Update conversation ID if it's the first message
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant message to the list
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        createdAt: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the list
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        createdAt: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    input,
    setInput,
    isLoading,
    sendMessage,
    conversationId,
    setConversationId
  };
};