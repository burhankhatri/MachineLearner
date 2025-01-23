import React, { useState } from 'react'
import { Editor } from '@monaco-editor/react'
import { Card } from './components/ui/card'
import Plot from 'react-plotly.js'
import clsx from 'clsx'
import { PlotData } from 'plotly.js'

interface Framework {
  id: 'tensorflow' | 'pytorch' | 'sklearn'
  name: string
  description: string
}

interface Metrics {
  accuracy?: number
  loss?: number
  precision?: number
  recall?: number
}

interface Progress {
  epoch: number
  loss: number
  accuracy?: number
}

interface Message {
  role: string
  content: string
}

const frameworks: Framework[] = [
  {
    id: 'tensorflow',
    name: 'TensorFlow',
    description: 'Deep learning framework by Google'
  },
  {
    id: 'pytorch',
    name: 'PyTorch',
    description: 'Deep learning framework by Facebook'
  },
  {
    id: 'sklearn',
    name: 'scikit-learn',
    description: 'Machine learning library for Python'
  }
]

export default function App() {
  const [selectedFramework, setSelectedFramework] = useState<Framework | null>(null)
  const [prompt, setPrompt] = useState('Create a neural network for image classification')
  const [code, setCode] = useState(`# Your Python code will appear here
import tensorflow as tf

# Example:
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(10, activation='softmax')
])`)
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [progress, setProgress] = useState<Progress[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [chatHistory, setChatHistory] = useState<Message[]>([])

  const handleFrameworkSelect = (frameworkId: string) => {
    setSelectedFramework(frameworks.find(f => f.id === frameworkId) || null)
    console.log(`Selected framework: ${frameworkId}`)
  }

  const handleGenerateCode = async () => {
    try {
      setIsLoading(true)
      setError(null)
      console.log('Generating code for prompt:', prompt)

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          prompt: `Using ${selectedFramework?.name}, ${prompt}`,
          chat_history: chatHistory
        })
      })

      if (!response.ok) throw new Error('Failed to generate code')
      
      const data = await response.json()
      setCode(data.code)
      
      // Update chat history
      setChatHistory([
        ...chatHistory,
        { role: 'user', content: prompt },
        { role: 'assistant', content: data.code }
      ])

      console.log('Code generated successfully')
    } catch (err) {
      console.error('Error generating code:', err)
      setError(err instanceof Error ? err.message : 'Failed to generate code')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRunCode = async () => {
    try {
      setIsLoading(true)
      setError(null)
      console.log('Running code...')

      const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      })

      if (!response.ok) throw new Error('Failed to run code')
      
      const result = await response.json()
      console.log('Code execution result:', result)

      if (result.error) {
        setError(result.error)
        // Try to fix the code
        const fixResponse = await fetch('/api/fix', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            code,
            error: result.error,
            chat_history: chatHistory
          })
        })

        if (fixResponse.ok) {
          const fixedCode = await fixResponse.json()
          setCode(fixedCode.code)
          setChatHistory([
            ...chatHistory,
            { role: 'user', content: `Fix error: ${result.error}` },
            { role: 'assistant', content: fixedCode.code }
          ])
        }
      } else {
        // Update metrics and progress
        if (result.metrics) setMetrics(result.metrics)
        if (result.progress) setProgress(result.progress)
      }
    } catch (err) {
      console.error('Error running code:', err)
      setError(err instanceof Error ? err.message : 'Failed to run code')
    } finally {
      setIsLoading(false)
    }
  }

  const handleOptimize = async () => {
    if (!metrics) return

    try {
      setIsLoading(true)
      setError(null)
      console.log('Optimizing code with metrics:', metrics)

      const response = await fetch('/api/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          metrics,
          chat_history: chatHistory
        })
      })

      if (!response.ok) throw new Error('Failed to optimize code')
      
      const data = await response.json()
      setCode(data.code)
      
      setChatHistory([
        ...chatHistory,
        { role: 'user', content: 'Optimize code' },
        { role: 'assistant', content: data.code }
      ])

      console.log('Code optimized successfully')
    } catch (err) {
      console.error('Error optimizing code:', err)
      setError(err instanceof Error ? err.message : 'Failed to optimize code')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">ML.new</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {!selectedFramework ? (
          <section className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4">
              What ML model do you want to build?
            </h2>
            <p className="text-muted-foreground mb-8">
              Describe your model, and we'll help you create it with your preferred framework
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {frameworks.map((framework) => (
                <button
                  key={framework.id}
                  onClick={() => handleFrameworkSelect(framework.id)}
                  className={clsx(
                    'p-6 rounded-xl border-2 transition-all hover:scale-105',
                    selectedFramework === framework
                      ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/20'
                      : 'border-zinc-800 hover:border-zinc-700 hover:bg-zinc-900'
                  )}
                >
                  <h4 className="text-xl font-semibold mb-2">{framework.name}</h4>
                  <p className="text-zinc-400">{framework.description}</p>
                </button>
              ))}
            </div>
          </section>
        ) : (
          <section>
            <Card className="p-4">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-lg font-medium mb-4">Code Editor</h3>
                  <Editor
                    height="600px"
                    defaultLanguage="python"
                    theme="vs-dark"
                    value={code}
                    onChange={(value) => setCode(value || '')}
                    options={{
                      fontSize: 14,
                      minimap: { enabled: false },
                      scrollBeyondLastLine: false,
                    }}
                  />
                </div>
                <div>
                  <h3 className="text-lg font-medium mb-4">Results</h3>
                  {/* Results display */}
                </div>
              </div>
            </Card>
          </section>
        )}
      </main>
    </div>
  )
} 