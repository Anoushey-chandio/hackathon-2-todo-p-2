'use client';

import React, { useState, useEffect, useRef } from 'react';
import { fetchClient } from '@/lib/api';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

export default function ChatWidget({ onTaskAdded }: { onTaskAdded?: () => void }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll: Naye messages aane par chat bottom par focus karegi
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    // User message ko UI mein turant add karein
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setLoading(true);

    try {
      // ✅ Updated endpoint URL to match backend
      const res = await fetchClient('/api/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: text, 
          conversation_id: conversationId 
        }),
      });

      if (!res.ok) throw new Error('Network response was not ok');

      const data = await res.json();
      
      // Assistant ka response add karein
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      
      // Conversation ID update
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }
      
      // Agar backend ne task add kiya hai, parent list refresh karein
      if (data.action_taken === 'task_added' && onTaskAdded) {
        onTaskAdded();
      }
    } catch (e) {
      console.error('Chat error:', e);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'I’m having trouble reaching the server. Please try again later.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end pointer-events-none">
      {isOpen && (
        <div className="pointer-events-auto mb-4 w-80 md:w-96 h-[500px] bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-800 flex flex-col overflow-hidden animate-in slide-in-from-bottom-5">
          
          {/* Header */}
          <div className="p-4 bg-purple-600 text-white flex justify-between items-center shadow-sm">
            <h3 className="font-bold">✨ Groq AI Assistant</h3>
            <button 
              onClick={() => setIsOpen(false)}
              className="hover:opacity-80 transition-opacity"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 bg-white dark:bg-gray-900" ref={scrollRef}>
            <MessageList messages={messages} loading={loading} />
          </div>

          {/* Input */}
          <div className="p-3 bg-gray-50 dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700">
            <MessageInput onSend={handleSend} disabled={loading} />
          </div>
        </div>
      )}

      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="pointer-events-auto w-14 h-14 bg-purple-600 text-white rounded-full shadow-lg flex items-center justify-center hover:scale-105 active:scale-95 transition-transform"
      >
        {isOpen ? '↓' : '💬'}
      </button>
    </div>
  );
}
