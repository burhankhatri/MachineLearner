import { useState } from 'react'
import Editor from '@monaco-editor/react'
import Plot from 'react-plotly.js'
import { clsx } from 'clsx'

const frameworks = [
  {
    id: 'tensorflow',
    name: 'TensorFlow',
    description: 'Deep Learning & Neural Networks',
    icon: '/img/tensorflow.svg'
  },
  {
    id: 'pytorch',
    name: 'PyTorch',
    description: 'Dynamic Neural Networks',
    icon: '/img/pytorch.svg'
  },
  {
    id: 'sklearn',
    name: 'scikit-learn',
    description: 'Classical ML Algorithms',
    icon: '/img/scikit.svg'
  }
]

export default function App() {
  const [selectedFramework, setSelectedFramework] = useState(null)
  const [code, setCode] = useState('')
  const [metrics, setMetrics] = useState({ accuracy: '-', loss: '-' })
  const [isLoading, setIsLoading] = useState(false)

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-sm border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold">ML.new</h1>
            <nav className="flex items-center space-x-4">
              <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                Documentation
              </a>
              <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                Examples
              </a>
              <a 
                href="https://github.com/yourusername/ml-new" 
                target="_blank"
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                </svg>
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-16">
        {/* Hero Section */}
        <section className="px-4 py-32 animate-fade-in">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-5xl font-bold mb-6">What ML model do you want to build?</h2>
            <p className="text-xl text-muted-foreground mb-12">
              Describe your model, and we'll help you create it with your preferred framework
            </p>

            {/* Framework Selection */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              {frameworks.map((framework) => (
                <button
                  key={framework.id}
                  onClick={() => setSelectedFramework(framework.id)}
                  className="w-full"
                >
                  <div
                    className={clsx(
                      'relative flex items-center space-x-4 p-4 rounded-xl border transition-all duration-200',
                      'bg-secondary hover:bg-secondary/60 border-border hover:border-border/60',
                      selectedFramework === framework.id && 'bg-primary/10 border-primary'
                    )}
                  >
                    <div className="w-12 h-12 flex items-center justify-center">
                      <img src={framework.icon} alt={framework.name} className="w-8 h-8" />
                    </div>
                    <div className="flex-1 text-left">
                      <h3 className="font-medium mb-1">{framework.name}</h3>
                      <p className="text-sm text-muted-foreground">{framework.description}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Model Interface */}
        {selectedFramework && (
          <section className="animate-slide-up">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Code Editor */}
                <div className="bg-secondary rounded-xl border border-border overflow-hidden">
                  <div className="border-b border-border p-4">
                    <div className="flex items-center justify-between">
                      <h3 className="font-medium">Code Editor</h3>
                      <div className="flex space-x-2">
                        <button 
                          onClick={() => {}} 
                          className="px-3 py-1.5 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg text-sm transition-colors"
                        >
                          Run
                        </button>
                        <button 
                          onClick={() => {}} 
                          className="px-3 py-1.5 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg text-sm transition-colors"
                        >
                          Optimize
                        </button>
                      </div>
                    </div>
                  </div>
                  <Editor
                    height="600px"
                    defaultLanguage="python"
                    theme="vs-dark"
                    value={code}
                    onChange={setCode}
                    options={{
                      fontSize: 14,
                      minimap: { enabled: false },
                      scrollBeyondLastLine: false,
                    }}
                  />
                </div>

                {/* Results Panel */}
                <div className="space-y-6">
                  {/* Metrics */}
                  <div className="bg-secondary rounded-xl border border-border p-6">
                    <h3 className="font-medium mb-4">Model Metrics</h3>
                    <div className="grid grid-cols-2 gap-6">
                      <div className="bg-background rounded-lg border border-border p-4">
                        <p className="text-sm text-muted-foreground mb-1">Accuracy</p>
                        <p className="text-2xl font-mono">{metrics.accuracy}</p>
                      </div>
                      <div className="bg-background rounded-lg border border-border p-4">
                        <p className="text-sm text-muted-foreground mb-1">Loss</p>
                        <p className="text-2xl font-mono">{metrics.loss}</p>
                      </div>
                    </div>
                  </div>

                  {/* Training Progress */}
                  <div className="bg-secondary rounded-xl border border-border p-6">
                    <h3 className="font-medium mb-4">Training Progress</h3>
                    <div className="h-64 bg-background rounded-lg border border-border">
                      <Plot
                        data={[
                          {
                            y: [0],
                            type: 'scatter',
                            mode: 'lines',
                            name: 'Loss',
                            line: { color: '#3B82F6' }
                          }
                        ]}
                        layout={{
                          paper_bgcolor: 'transparent',
                          plot_bgcolor: 'transparent',
                          margin: { t: 0, r: 0, l: 30, b: 30 },
                          xaxis: {
                            showgrid: true,
                            gridcolor: 'rgba(39, 39, 42, 0.4)',
                            zeroline: false,
                            showline: false,
                            tickfont: { color: '#A1A1AA' }
                          },
                          yaxis: {
                            showgrid: true,
                            gridcolor: 'rgba(39, 39, 42, 0.4)',
                            zeroline: false,
                            showline: false,
                            tickfont: { color: '#A1A1AA' }
                          }
                        }}
                        config={{ displayModeBar: false }}
                        className="w-full h-full"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Loading Overlay */}
      {isLoading && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-secondary p-8 rounded-xl border border-border animate-fade-in">
            <div className="flex items-center space-x-4">
              <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
              <p className="text-muted-foreground">Processing...</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 