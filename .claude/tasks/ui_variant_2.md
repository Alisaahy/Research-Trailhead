# UI Variant 2 - Sage Green & Gradient Theme

## Plan

### Design Approach
- **Color Palette:**
  - Primary: Sage Green (#8B9D83)
  - Background: White (#FFFFFF)
  - Text: Charcoal (#2D3748)
  - Gradients: Sage to white (subtle)
  - Accents: Darker sage for hover states

- **Spacing System:** 8pt (8, 16, 24, 32, 40, 48px)
- **Typography:** System fonts, 16px base, 24px line-height
- **Shadows:** Soft, subtle for depth
- **Borders:** Sage green frames

### Implementation Steps

1. **HTML Structure**
   - Single-page layout with 5 workflow steps
   - Progress indicator at top
   - Each step as a section (show/hide based on state)
   - Result containers with gradient backgrounds

2. **Styling (Tailwind + Custom)**
   - Import Tailwind via CDN
   - Define custom sage green colors
   - Gradient utilities for cards
   - 8pt spacing throughout
   - Soft shadows on cards
   - Sage borders on containers

3. **JavaScript Functionality**
   - State management for workflow steps
   - API integration for all 5 endpoints
   - Form validation
   - Loading states with sage spinners
   - Error handling
   - Smooth transitions between steps

4. **UI Components**
   - Sage green buttons with hover effects
   - Gradient result cards
   - Checkbox styling (sage accents)
   - Progress bars (sage fill)
   - File upload styling
   - Textarea with sage borders

### Workflow Flow
1. User Profile → Create profile → Show success
2. Upload Paper → Get job_id → Show job_id
3. Quick Read → Select topics → Show analysis
4. Select Ideas → Choose 3 → Research button
5. Final Results → Show ranked ideas with scores

## Implementation Details

### Custom Tailwind Config
```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        sage: {
          50: '#f6f7f6',
          100: '#e3e7e2',
          200: '#c7cfc5',
          300: '#a5b29f',
          400: '#8b9d83',
          500: '#6f8267',
          600: '#5a6852',
          700: '#495344',
          800: '#3d4539',
          900: '#343a31',
        }
      }
    }
  }
}
```

### Key Interactions
- Step transitions: Fade in/out with 300ms duration
- Button hover: Darken sage color
- Checkbox selection: Sage checkmark
- Loading: Sage spinner animation
- Success states: Green gradient background

### Testing Checklist
- [ ] All 5 steps work sequentially
- [ ] API calls function correctly
- [ ] Validation prevents invalid inputs
- [ ] Gradients render smoothly
- [ ] 8pt spacing consistent
- [ ] Sage theme applied throughout
- [ ] Responsive on mobile
- [ ] Error states display properly

---

## Implementation Complete

### File Created
- `/Users/alisa/Documents/Hackthon/ui_iterations/ui_2.html`

### Features Implemented

**Design System:**
- 8pt spacing system (8, 12, 16, 24px multiples)
- Sage green color palette (#8B9D83 primary)
- Gradient backgrounds (sage to white)
- Soft shadows for depth
- Sage green borders on main containers
- White background throughout

**UI Components:**
- Progress indicator with 5 steps (sage highlighting)
- Sage green buttons with hover states
- Gradient result cards
- Custom checkboxes with sage accents
- Gradient progress bars for scores
- Loading spinners (sage themed)
- Smooth fade-in transitions (300ms)

**Workflow Steps:**
1. **User Profile:** Manual input or Google Scholar URL, experience level dropdown
2. **Upload Paper:** File upload, auto-detected topics display, manual topic addition
3. **Quick Analysis:** Paper summary, key concepts, research ideas with selection
4. **Idea Selection:** Users select exactly 3 ideas via checkboxes
5. **Final Results:** Ranked ideas with gradient cards, score bars, references

**Technical Details:**
- Single HTML file with embedded CSS and JavaScript
- Tailwind CSS via CDN with custom sage colors
- Custom gradients using CSS
- Fade-in animations for smooth transitions
- API integration to http://localhost:5001
- Form validation and error handling
- Loading states with sage spinners
- Scrollbar hidden for clean mobile look
- Progress bars using sage gradient fills

**Color Usage:**
- Background: White (#FFFFFF)
- Primary: Sage #8B9D83
- Gradients: Sage tints (#f6f7f6 → #e3e7e2 → white)
- Text: Charcoal (#2D3748, gray-700, gray-800)
- Accents: Sage variants for hover and active states

**Spacing Adherence:**
- All padding/margin values: 8, 12, 16, 24px
- Touch targets: 48px+ for buttons
- Consistent gap spacing: 8, 16, 24px
- Line heights aligned to 24px grid

The UI maintains a calm, natural aesthetic with the sage green theme while providing full functionality for the 5-step research discovery workflow.
