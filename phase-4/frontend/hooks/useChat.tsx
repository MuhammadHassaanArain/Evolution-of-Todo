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
      // Get the authentication token from localStorage
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');

      const response = await fetch(`/api/conversations/${id}/messages`, {
        headers: {
          ...(token && { 'Authorization': `Bearer ${token}` })
        }
      });

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          // Clear any invalid tokens and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('token');

          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
          throw new Error(`Authentication error: ${response.status}`);
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }

      const data = await response.json();
      // Transform API response to match our Message interface
      const transformedMessages: Message[] = data.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        createdAt: msg.created_at
      }));
      setMessages(transformedMessages);
    } catch (error: any) {
      console.error('Error loading conversation messages:', error);

      if (error.message && (error.message.includes('401') || error.message.includes('Authentication error'))) {
        // Add authentication error message
        setMessages([
          {
            id: 1,
            role: 'assistant',
            content: 'Your session has expired. Please log in again.',
            createdAt: new Date().toISOString(),
          }
        ]);
      } else {
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
      // Get the authentication token from localStorage
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');

      // Call the chat API
      const response = await fetch( `${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: messageToSend,
        }),
        
      });

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          throw new Error(`Authentication error: ${response.status}`);
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
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
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Handle specific authentication errors
      if (error.message && (error.message.includes('401') || error.message.includes('Unauthorized'))) {
        // Clear any invalid tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('token');

        // Redirect to login page
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }

        // Add authentication error message
        const errorMessage: Message = {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Your session has expired. Please log in again.',
          createdAt: new Date().toISOString(),
        };

        setMessages(prev => [...prev, errorMessage]);
      } else {
        // Add generic error message to the list
        const errorMessage: Message = {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          createdAt: new Date().toISOString(),
        };

        setMessages(prev => [...prev, errorMessage]);
      }
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