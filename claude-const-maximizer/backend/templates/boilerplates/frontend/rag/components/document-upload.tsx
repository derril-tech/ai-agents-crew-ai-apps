"use client"

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface UploadedFile {
  id: string
  name: string
  size: number
  status: 'uploading' | 'success' | 'error'
  progress?: number
}

interface DocumentUploadProps {
  onUploadComplete?: (files: UploadedFile[]) => void
  maxFiles?: number
  acceptedTypes?: string[]
}

export function DocumentUpload({ 
  onUploadComplete, 
  maxFiles = 10,
  acceptedTypes = ['.pdf', '.txt', '.doc', '.docx', '.md']
}: DocumentUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const { toast } = useToast()

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = acceptedFiles.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      status: 'uploading' as const,
      progress: 0
    }))

    setUploadedFiles(prev => [...prev, ...newFiles])

    // Simulate upload process
    for (const file of acceptedFiles) {
      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error('Upload failed')
        }

        // Update file status to success
        setUploadedFiles(prev => 
          prev.map(f => 
            f.name === file.name 
              ? { ...f, status: 'success' as const, progress: 100 }
              : f
          )
        )

        toast({
          title: "Upload successful",
          description: `${file.name} has been uploaded and processed.`,
        })

      } catch (error) {
        // Update file status to error
        setUploadedFiles(prev => 
          prev.map(f => 
            f.name === file.name 
              ? { ...f, status: 'error' as const }
              : f
          )
        )

        toast({
          title: "Upload failed",
          description: `Failed to upload ${file.name}.`,
          variant: "destructive",
        })
      }
    }

    onUploadComplete?.(uploadedFiles)
  }, [uploadedFiles, onUploadComplete, toast])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/markdown': ['.md']
    }
  })

  const removeFile = (fileId: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="w-5 h-5" />
            Upload Documents
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-950'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
            {isDragActive ? (
              <p className="text-lg font-medium">Drop the files here...</p>
            ) : (
              <div>
                <p className="text-lg font-medium mb-2">
                  Drag & drop files here, or click to select
                </p>
                <p className="text-sm text-gray-500">
                  Supported formats: {acceptedTypes.join(', ')}
                </p>
                <p className="text-sm text-gray-500">
                  Max files: {maxFiles}
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Uploaded Files</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {uploadedFiles.map((file) => (
                <div
                  key={file.id}
                  className="flex items-center justify-between p-3 border rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <File className="w-5 h-5 text-gray-500" />
                    <div>
                      <p className="font-medium">{file.name}</p>
                      <p className="text-sm text-gray-500">
                        {formatFileSize(file.size)}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    {file.status === 'uploading' && (
                      <div className="flex items-center gap-2">
                        <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                        <span className="text-sm text-gray-500">
                          {file.progress}%
                        </span>
                      </div>
                    )}
                    
                    {file.status === 'success' && (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    )}
                    
                    {file.status === 'error' && (
                      <AlertCircle className="w-5 h-5 text-red-500" />
                    )}
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeFile(file.id)}
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
