import React, { useState } from 'react';
import { Send } from 'lucide-react';

interface MessageInputProps {
  input: string;
  setInput: (input: string) => void;
  isLoading: boolean;
  onSend: () => void;
}

export const MessageInput = ({
  input,
  setInput,
  isLoading,
  onSend
}: MessageInputProps) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        disabled={isLoading}
        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        aria-label="Type your message"
      />
      <button
        type="submit"
        disabled={!input.trim() || isLoading}
        className={`p-2 rounded-lg ${
          input.trim() && !isLoading
            ? 'bg-blue-500 text-white hover:bg-blue-600'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
        aria-label="Send message"
      >
        {isLoading ? (
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
        ) : (
          <Send size={20} />
        )}
      </button>
    </form>
  );
};