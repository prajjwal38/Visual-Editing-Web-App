# Visual Editor - Frontend

A modern, professional video editing UI built with React, TypeScript, and Tailwind CSS.

## Features

- **Project Dashboard**: Create, view, and manage video editing projects
- **Timeline Editor**: Visual timeline with layer management
- **Effects Panel**: Apply and configure effects (Blur, Brightness, Vintage, Sharpen, Crop)
- **Export Interface**: Export projects to multiple formats (MP4, MOV, AVI, WebM, GIF)
- **Resolution Presets**: Quick selection for Instagram, YouTube, TikTok, and more
- **Responsive Design**: Optimized for desktop and tablet

## Tech Stack

- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Vite**: Lightning-fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Lucide React**: Beautiful icon set

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                 # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Card.tsx
│   │   ├── projects/           # Project-related components
│   │   │   ├── CreateProjectModal.tsx
│   │   │   └── ProjectCard.tsx
│   │   └── editor/             # Editor components
│   │       ├── Timeline.tsx
│   │       ├── LayerItem.tsx
│   │       ├── EffectsPanel.tsx
│   │       ├── AddLayerModal.tsx
│   │       └── ExportPanel.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx       # Project dashboard
│   │   └── Editor.tsx          # Video editor
│   ├── services/
│   │   └── api.ts              # API client
│   ├── store/
│   │   └── useStore.ts         # Global state management
│   ├── types/
│   │   └── index.ts            # TypeScript types
│   ├── App.tsx                 # Main app component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── public/                     # Static assets
├── index.html                  # HTML template
├── package.json
├── vite.config.ts             # Vite configuration
├── tailwind.config.js         # Tailwind configuration
└── tsconfig.json              # TypeScript configuration
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Open http://localhost:3000 in your browser

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with the FastAPI backend via Axios. The Vite dev server proxies `/api` requests to `http://localhost:8000`.

### API Endpoints Used

- `POST /api/v1/projects/` - Create project
- `GET /api/v1/projects/` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `DELETE /api/v1/projects/{id}` - Delete project
- `POST /api/v1/projects/{id}/timeline/layers` - Add layer
- `GET /api/v1/effects` - List effects
- `POST /api/v1/projects/{id}/layers/{layer_id}/effects` - Apply effect
- `POST /api/v1/projects/{id}/export` - Export project

## State Management

Uses Zustand for simple, lightweight state management:

```typescript
const { currentProject, setCurrentProject } = useStore();
```

### Store Structure

- `projects`: List of all projects
- `currentProject`: Currently selected project
- `availableEffects`: List of available effects
- `selectedLayerId`: Currently selected layer
- `isLoading`: Loading state
- `error`: Error messages

## Component Overview

### Pages

- **Dashboard**: Main landing page showing all projects
- **Editor**: Video editing workspace with timeline, effects, and canvas

### UI Components

- **Button**: Reusable button with variants (primary, secondary, danger, ghost)
- **Input**: Form input with label and error handling
- **Modal**: Dialog component for forms and confirmations
- **Card**: Container component for content cards

### Feature Components

- **CreateProjectModal**: Form to create new projects with resolution presets
- **ProjectCard**: Display project information on dashboard
- **Timeline**: Visual timeline showing all layers
- **LayerItem**: Individual layer representation
- **EffectsPanel**: Browse and apply effects to layers
- **AddLayerModal**: Form to add new layers
- **ExportPanel**: Export project configuration and execution

## Styling

Uses Tailwind CSS utility classes. Custom theme configuration in `tailwind.config.js`:

- Primary color: Blue (customizable)
- Responsive breakpoints
- Custom utilities for animations

## Development Guidelines

### Code Style

- Use TypeScript for type safety
- Follow React hooks best practices
- Use functional components
- Prefer composition over inheritance
- Keep components small and focused

### Adding a New Page

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Update navigation if needed

### Adding a New API Endpoint

1. Add TypeScript types to `src/types/index.ts`
2. Add API function to `src/services/api.ts`
3. Use in components with error handling

## Building for Production

1. Build the app:
   ```bash
   npm run build
   ```

2. Preview the build:
   ```bash
   npm run preview
   ```

3. Deploy the `dist/` folder to your hosting service

## Future Enhancements

- [ ] Real-time preview rendering
- [ ] Drag-and-drop file uploads
- [ ] Timeline scrubbing with playhead
- [ ] Keyboard shortcuts
- [ ] Undo/redo functionality
- [ ] Template library
- [ ] Collaborative editing
- [ ] Cloud storage integration
- [ ] Progress indicators for export

## Troubleshooting

### Backend API not reachable

Make sure the backend is running on http://localhost:8000:
```bash
cd ..
python main.py
```

### Port 3000 already in use

Change the port in `vite.config.ts`:
```typescript
server: {
  port: 3001, // or any other port
}
```

## License

MIT License

---

Built with React, TypeScript, and Tailwind CSS
