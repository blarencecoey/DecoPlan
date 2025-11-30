# ChatBox Feature Guide

## Overview

The DecoPlan demo now includes an **AI Design Assistant Chatbox** that allows users to request different room styles using natural language. The chatbox uses the mock RAG system to detect room styles from user queries and retrieve appropriate furniture.

## New Features

### 1. AI Chatbox Interface

Located in the **upper half** of the right panel, the chatbox provides:

- **Natural Language Input**: Type requests like "Generate a Japanese style living room"
- **Chat History**: View conversation with the AI assistant
- **Quick Prompts**: One-click buttons for common room styles
- **Real-time Responses**: AI responds with confirmation and furniture count
- **Loading States**: Visual feedback while generating rooms

### 2. Style Detection System

The RAG system now automatically detects room styles from queries:

**Supported Styles:**
- **Japanese**: Keywords: japanese, japan, zen, tatami
- **Modern**: Default style (keywords: modern, contemporary)
- **Minimalist**: Keywords: minimalist, minimal
- **Scandinavian**: Keywords: scandinavian, nordic
- **Industrial**: Keywords: industrial
- **Traditional**: Keywords: traditional

### 3. Japanese-Style Furniture Database

Added 10 new Japanese-style furniture items:

1. **Chabudai Low Table** - Traditional low dining table
2. **Futon Seating** - Low-profile Japanese seating
3. **Tansu Storage Cabinet** - Traditional chest of drawers
4. **Andon Floor Lamp** - Paper lantern lamp
5. **Shoji Screen Shelf** - Display shelf with sliding doors
6. **Tea Ceremony Table** - Small low table
7. **Zaisu Floor Chairs** (×2) - Legless floor chairs
8. **Kotatsu Table** - Heated table with blanket
9. **Bonsai Display Stand** - Decorative stand

## How to Use

### Using the Chatbox

1. **Start a Conversation**:
   - Type your request in the input box at the bottom
   - Example: "Generate a Japanese style living room"
   - Press Enter or click "Send"

2. **Use Quick Prompts**:
   - Click pre-made buttons for instant requests
   - Available when chat is empty or after starting conversation
   - Options: Japanese, Modern, Minimalist

3. **View Responses**:
   - User messages appear in purple on the right
   - AI responses appear in gray on the left
   - Each message shows timestamp

4. **Explore Generated Rooms**:
   - Furniture automatically appears in 3D viewer
   - Use furniture panel (bottom half) to toggle items
   - Check statistics panel for room coverage

### Example Queries

**Japanese Style:**
```
"Generate a Japanese style living room"
"Show me a zen-inspired room"
"Create a traditional Japanese space"
```

**Other Styles:**
```
"Generate a modern minimalist room"
"Show me a scandinavian living room"
"Create an industrial loft space"
```

**General Requests:**
```
"Show me HDB living room furniture"
"Generate a cozy living space"
"Create a compact room design"
```

## UI Layout

```
┌─────────────────────────────────────────────┬──────────────────┐
│                                             │   AI Chatbox     │
│                                             │   (Upper Half)   │
│          3D Room Viewer (70%)               ├──────────────────┤
│                                             │  Furniture Panel │
│                                             │   (Lower Half)   │
└─────────────────────────────────────────────┴──────────────────┘
```

**Right Panel Split (50/50):**
- **Top Half**: AI Design Assistant Chatbox
- **Bottom Half**: Furniture List & Controls

## Features in Detail

### Chat Message Types

1. **User Messages** (Purple, Right-aligned):
   - Your requests and queries
   - Shows send time

2. **Assistant Messages** (Gray, Left-aligned):
   - AI responses with furniture count
   - Style confirmation
   - Shows receive time

3. **System Messages** (Blue, Left-aligned):
   - Error notifications
   - System updates

### Quick Prompt Buttons

**Initial State (Empty Chat):**
- "Japanese style living room"
- "Modern minimalist room"
- "Traditional HDB furniture"

**Active Chat State:**
- Japanese
- Modern
- Minimalist

### Loading States

- **Input Disabled**: During furniture retrieval
- **Send Button**: Shows spinner with "Generating..." text
- **Quick Prompts**: Disabled while loading

### Auto-scroll

Chat automatically scrolls to newest message when:
- User sends a message
- AI responds
- New message arrives

## Technical Implementation

### New Components

**`components/ChatBox.tsx`**
- Main chatbox UI component
- Message rendering
- Input handling
- Quick prompt buttons

**`types/chat.ts`**
- ChatMessage interface
- MessageRole type
- RoomStyle type
- StyleQuery interface

### Updated Files

**`lib/mockRAG.ts`**
- `detectRoomStyle()`: Detects style from query
- `getFurnitureByStyle()`: Returns appropriate database
- Updated `retrieveFurniture()`: Uses style detection

**`lib/furnitureData.ts`**
- `JAPANESE_FURNITURE_DATABASE`: New furniture set

**`app/page.tsx`**
- Chat message state
- `handleSendMessage()`: Processes chat requests
- Updated layout with split panel

## Tips for Best Experience

1. **Be Specific**: Mention the style explicitly for best results
   - Good: "Generate a Japanese style living room"
   - Okay: "Show me a zen room"

2. **Use Keywords**: Include style keywords for accurate detection
   - Japanese: zen, tatami, traditional
   - Modern: contemporary, sleek
   - Minimalist: minimal, simple

3. **Explore Multiple Styles**: Try different requests to see variety
   - Compare Japanese vs Modern layouts
   - Notice differences in furniture heights and types

4. **Use Quick Prompts**: For fastest results
   - Click buttons for instant generation
   - Perfect for demonstrations

## Future Enhancements

Potential improvements:
- More room styles (Bohemian, Art Deco, etc.)
- More furniture databases per style
- Advanced style mixing
- Room size customization via chat
- Color scheme requests
- Furniture arrangement suggestions
- Save/load conversations
- Export room designs

## Troubleshooting

**Chat not responding:**
- Check console for errors
- Ensure internet connection (even for mock RAG)
- Refresh page and try again

**Furniture not changing:**
- Wait for "Ready" status
- Check loading indicator
- Verify furniture panel shows new items

**Style not detected:**
- Use explicit keywords
- Try alternative phrasings
- Check supported styles list

---

**Enjoy creating beautiful rooms with the AI Design Assistant!**
