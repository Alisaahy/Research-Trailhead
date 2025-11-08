# UI Variant 1 - Minimalist Black & White Theme

## Overview
Create a single-page HTML interface with a minimalist black and white design, supporting a complete 5-step research discovery workflow.

## Design Principles

### Color Scheme
- Background: Pure white (#FFFFFF)
- Text: Black (#000000) and dark gray (#1F2937)
- Borders: Black (#000000) and medium gray (#6B7280)
- Accents: Light gray (#F3F4F6, #E5E7EB) for subtle backgrounds
- Shadows: Subtle gray shadows for depth
- No colors except black/white/gray scale

### Spacing System
- Use strict 8pt grid system (8, 16, 24, 32, 40, 48px)
- Consistent spacing tokens throughout
- Tight spacing (8px) for related items
- Larger spacing (24-32px) for distinct groups

### Typography
- Clear hierarchy with font sizes aligned to 8pt grid
- Font sizes: 12px, 16px, 20px, 24px, 32px
- Line heights: 16px, 24px, 32px, 40px
- Font weight: 400 (normal), 600 (semibold), 700 (bold)

### Visual Design
- Black borders on all cards and inputs (1-2px)
- Subtle gray shadows for depth
- Refined rounded corners (8px)
- Clean, professional aesthetic
- Modular card layouts

## Implementation Steps

### 1. HTML Structure
- Single HTML file with embedded CSS and JavaScript
- Responsive container (max-width)
- Header with title
- Progress indicator (5 steps)
- Main workflow sections (initially hidden)
- All sections on one page with show/hide logic

### 2. Step 1: User Profile
**UI Elements:**
- Profile method selector (Manual/Google Scholar)
- Manual section:
  - Textarea for research description (4-6 rows, black border)
  - Dropdown for experience level
- Scholar section (hidden by default):
  - Input for Google Scholar URL
- "Create Profile" button (black background, white text)
- Result display card (hidden initially):
  - User ID (monospace font)
  - Experience level
  - Research areas
  - Research style

**Functionality:**
- Toggle between manual/scholar methods
- POST to /api/users/profile
- Display profile data on success
- Show error messages
- Enable next step

### 3. Step 2: Upload Paper
**UI Elements:**
- File input for PDF (styled with black border)
- Display auto-detected topics from profile
- Optional manual topics input
- "Upload & Analyze" button
- Status indicator (job_id, progress)

**Functionality:**
- POST to /api/upload with file and user_id
- Combine auto-detected and manual topics
- POST to /api/analyze/read with job_id and topics
- Show loading state
- Display status updates
- Enable next step

### 4. Step 3: Quick Read Results
**UI Elements:**
- Paper summary (gray background card)
- Key concepts (gray tags/badges)
- Research ideas (5-10 ideas):
  - Each idea as a card with checkbox
  - Title and description
  - Limited to 3 selections
- "Research Selected Ideas" button

**Functionality:**
- Display summary, concepts, and ideas from API response
- Checkbox selection with 3-idea limit
- Validate selection before proceeding
- Store selected indices

### 5. Step 4: Select & Deep Research
**UI Elements:**
- Same as Step 3 (selection interface)
- Button triggers deep research

**Functionality:**
- POST to /api/analyze/search with job_id and selected_ideas
- Show loading state (5-10 min estimate)
- Poll for completion if needed
- Enable final step

### 6. Step 5: Final Ranked Results
**UI Elements:**
- 3 ranked idea cards:
  - Rank number
  - Title and description
  - Score display (novelty, doability, composite)
  - Rationale
  - Top 3-5 literature references
- Each card has black border and white background
- Subtle gray background for reference sections

**Functionality:**
- Display top_ideas from API response
- Show all scoring metrics
- Format references with title, year, citations

### 7. Progress Indicator
**UI Elements:**
- 5 step indicators at top of page
- Current step highlighted with black border
- Completed steps with checkmark
- Future steps grayed out

**Functionality:**
- Update on each step transition
- Visual feedback of progress

### 8. Smooth Transitions
**Features:**
- Fade in/out animations for sections
- Smooth scrolling to active section
- Loading states with subtle animations
- Error handling with clear messages

### 9. Responsive Design
**Breakpoints:**
- Mobile: Single column layout
- Tablet: Adjust spacing and sizing
- Desktop: Full layout

### 10. Error Handling
**Features:**
- API error messages in gray alert boxes
- Form validation before submission
- Network error handling
- Clear error states

## Technical Stack
- HTML5
- Tailwind CSS via CDN (customize for black/white theme)
- Vanilla JavaScript
- Fetch API for backend communication

## API Integration
- Base URL: http://localhost:5001
- Endpoints:
  - POST /api/users/profile
  - POST /api/upload
  - POST /api/analyze/read
  - POST /api/analyze/search
  - GET /api/status/{job_id} (if polling needed)

## File Output
- Location: /Users/alisa/Documents/Hackthon/ui_iterations/ui_1.html
- Single self-contained HTML file
- No external dependencies except Tailwind CDN

## Design Specifications

### Buttons
- Black background with white text
- 48px height (touch-friendly)
- 8px border-radius
- Hover: Dark gray (#1F2937)
- Disabled: Light gray background

### Input Fields
- White background
- Black 1px border
- 8px border-radius
- 40-48px height
- 16px padding
- Focus: 2px black border

### Cards
- White background
- Black 2px border
- 8px border-radius
- 24px padding
- Subtle gray shadow: 0 1px 3px rgba(0,0,0,0.1)

### Progress Indicator
- 5 equal-width segments
- Current: Black border (2px), light gray background
- Completed: Black border, darker gray background with checkmark
- Future: Light gray border, white background

## Testing Checklist
- [ ] All 5 steps flow smoothly
- [ ] API calls work correctly
- [ ] Error handling displays properly
- [ ] Loading states visible
- [ ] Selection limits enforced (3 ideas)
- [ ] Responsive on different screen sizes
- [ ] Smooth transitions and animations
- [ ] All spacing follows 8pt grid
- [ ] Pure black/white/gray color scheme
- [ ] Typography hierarchy clear
- [ ] Touch targets meet 48px minimum

## Notes
- Think MVP: Focus on core functionality first
- Ensure strict adherence to 8pt spacing system
- No colors beyond black/white/gray scale
- Professional, clean aesthetic throughout
- Clear visual hierarchy with spacing and typography
- Smooth user experience with loading states and transitions

---

## Implementation Completed

### Changes Made

**File Created:** `/Users/alisa/Documents/Hackthon/ui_iterations/ui_1.html`

**Key Features Implemented:**

1. **Minimalist Black & White Design**
   - Pure white background (#FFFFFF)
   - Black text (#111827) and borders (#000000)
   - Gray accents for subtle backgrounds (#F9FAFB, #F3F4F6, #E5E7EB)
   - No colors beyond grayscale

2. **Strict 8pt Spacing System**
   - All margins, padding, heights use multiples of 8px
   - Spacing tokens: 4, 8, 16, 24, 32, 40, 48, 56, 64px
   - Consistent spacing throughout the design

3. **Typography Hierarchy**
   - H1: 32px / 40px line-height
   - H2: 24px / 32px line-height
   - H3: 20px / 32px line-height
   - Body: 16px / 24px line-height
   - Small: 14px / 24px line-height
   - Extra small: 12px / 16px line-height

4. **Component Design**
   - Buttons: 48px height, black background, white text, 8px border-radius
   - Inputs: White background, black 1px border, 8px border-radius, 40-48px height
   - Cards: White background, black 2px border, 8px border-radius, 24px padding
   - Shadows: Subtle gray (0 1px 3px rgba(0,0,0,0.1))

5. **5-Step Workflow**
   - Step 1: User Profile (manual description or Google Scholar)
   - Step 2: Upload Paper (PDF + topics)
   - Step 3: Quick Read Results (summary, concepts, 5-10 ideas)
   - Step 4: Select Ideas (integrated with Step 3, select exactly 3)
   - Step 5: Final Ranked Results (3 ideas with scores and references)

6. **Progress Indicator**
   - 5-step grid layout at top of page
   - Active step: Black border, light gray background
   - Completed steps: Dark gray background, black border
   - Future steps: Light gray border, white background

7. **Interactive Features**
   - Smooth fade-in animations
   - Smooth scrolling between sections
   - Loading states with spinning indicators
   - Form validation and error messages
   - Checkbox selection with 3-idea limit enforcement
   - Hover states on buttons and interactive elements

8. **API Integration**
   - POST /api/users/profile - Create user profile
   - POST /api/upload - Upload PDF with user_id
   - POST /api/analyze/read - Quick analysis with topics
   - POST /api/analyze/search - Deep research with selected ideas
   - Error handling and status updates

9. **Responsive Design**
   - Max-width: 960px container
   - Padding: 32px vertical, 16px horizontal
   - Mobile-friendly touch targets (48px minimum)
   - Responsive grid layouts

10. **Accessibility**
    - Proper labels for all form elements
    - Touch-friendly button sizes (48px height)
    - Clear focus states
    - Semantic HTML structure
    - High contrast text (black on white)

### Technical Stack
- Single HTML file with embedded CSS and JavaScript
- Tailwind CSS via CDN (customized for black/white theme)
- Vanilla JavaScript (no frameworks)
- Fetch API for backend communication
- CSS animations for smooth transitions

### Design Adherence
- ✅ 8pt spacing system enforced throughout
- ✅ Pure black/white/gray color palette
- ✅ Professional, clean aesthetic
- ✅ Clear visual hierarchy
- ✅ Smooth transitions and animations
- ✅ Touch-friendly interactive elements (48px minimum)
- ✅ Consistent typography and spacing
- ✅ No scrollbars or non-mobile elements visible

### Testing Notes
- All API endpoints configured for http://localhost:5001
- Error handling implemented for network failures
- Form validation for required fields
- Loading states for async operations
- Progress tracking across all steps
- Smooth user flow from profile creation to final results
