import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, X, Send, Droplets, Sprout, Cloud } from 'lucide-react';

const AssistantBubble = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Hi! I\'m your agriculture assistant. How can I help you today?',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const quickSuggestions = [
    { icon: Droplets, label: 'Irrigation', query: 'Tell me about irrigation scheduling' },
    { icon: Sprout, label: 'Fertilizer', query: 'Recommend fertilizer for my crops' },
    { icon: Cloud, label: 'Weather', query: 'Check weather forecast' },
  ];

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: text.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');

    // Simulate bot response
    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: `I received your request about "${text.trim()}". Let me help you with that!`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, botMessage]);
    }, 800);
  };

  const handleQuickSuggestion = (query) => {
    handleSendMessage(query);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="mb-4 w-96 h-[600px] bg-white/90 backdrop-blur-xl rounded-2xl shadow-depth flex flex-col overflow-hidden border border-sage-200/50"
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-primary-500 to-emerald-600 p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-white rounded-2xl flex items-center justify-center shadow-lg">
                  <Sprout className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-white font-semibold text-lg">AgriBot</h3>
                  <p className="text-primary-100 text-xs">Always here to help</p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-white hover:bg-white/20 rounded-full p-2 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Quick Suggestions */}
            <div className="p-4 bg-cream-50/50 backdrop-blur-sm border-b border-sage-200/50">
              <p className="text-xs text-sage-600 mb-2 font-medium">Quick Actions:</p>
              <div className="flex gap-2">
                {quickSuggestions.map((suggestion, index) => {
                  const Icon = suggestion.icon;
                  return (
                    <button
                      key={index}
                      onClick={() => handleQuickSuggestion(suggestion.query)}
                      className="flex-1 flex flex-col items-center gap-1 p-2 bg-white/80 backdrop-blur-sm border border-sage-300 rounded-xl hover:border-primary-500 hover:bg-primary-50 transition-all group hover:scale-105"
                    >
                      <Icon className="w-5 h-5 text-sage-600 group-hover:text-primary-600" />
                      <span className="text-xs text-sage-700 group-hover:text-primary-700">
                        {suggestion.label}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Chat History */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-br from-cream-50/30 to-white">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                      message.type === 'user'
                        ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-br-sm shadow-lg'
                        : 'bg-white/80 backdrop-blur-sm text-sage-800 rounded-bl-sm shadow-soft border border-sage-200/50'
                    }`}
                  >
                    <p className="text-sm leading-relaxed">{message.text}</p>
                    <p
                      className={`text-xs mt-1 ${
                        message.type === 'user' ? 'text-primary-100' : 'text-sage-500'
                      }`}
                    >
                      {new Date(message.timestamp).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </p>
                  </div>
                </motion.div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Box */}
            <div className="p-4 bg-white/80 backdrop-blur-sm border-t border-sage-200/50">
              <div className="flex gap-2 items-end">
                <div className="flex-1 relative">
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message..."
                    className="w-full px-4 py-3 pr-12 border border-sage-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none bg-white/80 text-sage-900 placeholder:text-sage-400"
                    rows="1"
                    style={{ maxHeight: '100px' }}
                  />
                </div>
                <button
                  onClick={() => handleSendMessage(inputValue)}
                  disabled={!inputValue.trim()}
                  className="bg-gradient-to-r from-primary-500 to-primary-600 text-white p-3 rounded-xl hover:shadow-lg disabled:bg-sage-300 disabled:cursor-not-allowed transition-all"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Button */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsOpen(!isOpen)}
        className="w-16 h-16 bg-gradient-to-r from-primary-500 to-emerald-600 text-white rounded-full shadow-depth hover:shadow-2xl flex items-center justify-center transition-all"
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.div
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <X className="w-7 h-7" />
            </motion.div>
          ) : (
            <motion.div
              key="open"
              initial={{ rotate: 90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <MessageCircle className="w-7 h-7" />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.button>

      {/* Notification Badge (optional - can be controlled by props) */}
      {!isOpen && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center"
        >
          <span className="text-white text-xs font-bold">1</span>
        </motion.div>
      )}
    </div>
  );
};

export default AssistantBubble;
