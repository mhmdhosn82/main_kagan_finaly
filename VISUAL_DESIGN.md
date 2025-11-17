# Visual Design Summary

## Kagan Business Management System - UI Design

### Color Scheme (Glassmorphism)

**Primary Gradient (Sidebar):**
- Start: #667eea (Purple-blue)
- End: #764ba2 (Purple)
- Effect: Semi-transparent overlay with glassmorphism

**Background Gradient (Main Content):**
- Light mode: Gray95 to White
- Content cards: Pure white with rounded corners (15px radius)

**Text Colors:**
- Primary headings: #2c3e50 (Dark blue-gray)
- Secondary text: #7f8c8d (Medium gray)
- Sidebar text: White

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    Main Window (1200x700)                       │
│  ┌──────────────┬──────────────────────────────────────────┐   │
│  │   Sidebar    │         Content Area                     │   │
│  │   (250px)    │         (Dynamic)                        │   │
│  │              │                                          │   │
│  │   کاگان      │   ┌──────────────────────────────────┐   │   │
│  │ مدیریت کسب  │   │                                  │   │   │
│  │    و کار     │   │     Module Content               │   │   │
│  │              │   │     (White rounded box)          │   │   │
│  │ ┌──────────┐ │   │                                  │   │   │
│  │ │ آرایشگاه │ │   │  بخش [Module Name]              │   │   │
│  │ └──────────┘ │   │  Description text                │   │   │
│  │ ┌──────────┐ │   │                                  │   │   │
│  │ │  کافه    │ │   │                                  │   │   │
│  │ └──────────┘ │   │                                  │   │   │
│  │ ┌──────────┐ │   │                                  │   │   │
│  │ │ گیم نت   │ │   └──────────────────────────────────┘   │   │
│  │ └──────────┘ │                                          │   │
│  │     ...      │                                          │   │
│  │ ┌──────────┐ │                                          │   │
│  │ │ تنظیمات  │ │                                          │   │
│  │ └──────────┘ │                                          │   │
│  └──────────────┴──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Login Dialog

```
┌─────────────────────────────────────┐
│        Login Dialog (400x500)       │
│                                     │
│  سیستم مدیریت کسب و کار کاگان      │
│     کافه - آرایشگاه - گیم نت       │
│                                     │
│     نام کاربری:                     │
│  ┌─────────────────────────────┐   │
│  │ نام کاربری خود را وارد...  │   │
│  └─────────────────────────────┘   │
│                                     │
│     رمز عبور:                       │
│  ┌─────────────────────────────┐   │
│  │ ••••••••                    │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │         ورود                │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

### Typography

**Fonts:**
- Primary: Vazir (Persian font)
- Sizes:
  - Title: 28px, Bold
  - Subtitle: 14px, Regular
  - Sidebar logo: 24px, Bold
  - Sidebar subtitle: 12px
  - Button text: 13px
  - Login title: 20px, Bold

### Component Styling

**Buttons (Sidebar Navigation):**
- Background: Transparent with white border (2px)
- Border color: rgba(255, 255, 255, 0.3)
- Border radius: 10px
- Hover: rgba(255, 255, 255, 0.2)
- Text: White, center-aligned
- Height: 40px

**Input Fields (Login):**
- Height: 40px
- Border radius: 10px
- Background: Semi-transparent white
- Border: Subtle white border

**Content Cards (Modules):**
- Background: White
- Border radius: 15px
- Padding: 40px 30px
- Shadow: Subtle for depth

### Responsive Behavior

- Minimum window size: 1200x700
- Sidebar: Fixed at 250px
- Content area: Flexible, fills remaining space
- Modules: Full width within content area
- Login dialog: Fixed at 400x500, centered on screen

### RTL (Right-to-Left) Support

- All text aligned right
- Navigation buttons aligned right
- Input fields support Persian input
- Layout flows from right to left
- Sidebar on the left (content on right in RTL)

### Module Consistency

All 12 modules follow the same pattern:
1. Large bold title in Persian (28px)
2. Description text below (14px)
3. White background with rounded corners
4. Consistent spacing (40px top, 20px bottom)
5. Ready for content expansion

### Accessibility

- High contrast text
- Clear visual hierarchy
- Consistent spacing
- Readable font sizes
- Intuitive navigation
- Keyboard support (Enter key on login)

### Technical Implementation

- Framework: CustomTkinter 5.2.1
- Base: tkinter (Python standard library)
- Images: Pillow 10.3.0
- Platform: Cross-platform (Windows, macOS, Linux)
- No C++ build tools required
- Pure Python implementation
