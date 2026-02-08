'use client';
import React, { useState, useEffect } from 'react';
import { X, Send, Loader2 } from 'lucide-react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChat } from '../../hooks/useChat';

interface Conversation {
  id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
}

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatPanel = ({ isOpen, onClose }: ChatPanelProps) => {
  const {
    messages,
    input,
    setInput,
    isLoading,
    sendMessage,
    conversationId,
    setConversationId
  } = useChat();

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [showConversations, setShowConversations] = useState(false);

  // Load conversations when the component mounts or when showConversations is true
  useEffect(() => {
    if (showConversations) {
      loadConversations();
    }
  }, [showConversations]);

  const loadConversations = async () => {
    try {
      // Get the authentication token from localStorage
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');

      const response = await fetch('/api/conversations', {
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
      setConversations(data);
    } catch (error: any) {
      console.error('Error loading conversations:', error);

      if (error.message && (error.message.includes('401') || error.message.includes('Authentication error'))) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
      }
    }
  };

  const selectConversation = (id: number) => {
    setConversationId(id);
    setShowConversations(false);
    // In a real implementation, you would load the messages for this conversation
  };

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-24 right-6 w-96 h-[500px] bg-white border border-gray-200 rounded-lg shadow-xl flex flex-col z-50">
      <div className="flex justify-between items-center p-4 border-b border-gray-200">
        <div className="flex space-x-2">
          <h2 className="text-lg font-semibold">Todo Assistant</h2>
          <button
            onClick={() => setShowConversations(!showConversations)}
            className="text-sm text-blue-600 hover:underline"
          >
            {showConversations ? 'Chat' : 'History'}
          </button>
        </div>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
          aria-label="Close chat"
        >
          <X size={20} />
        </button>
      </div>

      {showConversations ? (
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          <h3 className="font-medium mb-2">Previous Conversations</h3>
          {conversations.length > 0 ? (
            <ul className="space-y-2">
              {conversations.map((conv) => (
                <li
                  key={conv.id}
                  className="p-2 bg-white border border-gray-200 rounded cursor-pointer hover:bg-gray-100"
                  onClick={() => selectConversation(conv.id)}
                >
                  <div className="font-medium">
                    {conv.title || `Conversation ${conv.id}`}
                  </div>
                  <div className="text-xs text-gray-500">
                    {new Date(conv.updated_at).toLocaleDateString()}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No previous conversations</p>
          )}
        </div>
      ) : (
        <>
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
            <MessageList messages={messages} isLoading={isLoading} />
          </div>

          <div className="p-4 border-t border-gray-200 bg-white">
            <MessageInput
              input={input}
              setInput={setInput}
              isLoading={isLoading}
              onSend={sendMessage}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default ChatPanel;