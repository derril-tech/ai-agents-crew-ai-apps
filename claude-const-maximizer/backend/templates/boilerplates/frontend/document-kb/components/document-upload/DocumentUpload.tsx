'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { 
  Upload, 
  FileText, 
  File, 
  CheckCircle, 
  AlertCircle, 
  X,
  Loader2,
  FileType,
  FileImage,
  FileSpreadsheet
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface DocumentUploadProps {
  onUpload?: (files: File[]) => void
  onProcessingComplete?: (results: ProcessingResult[]) => void
  maxFiles?: number
  maxSize?: number
  acceptedTypes?: string[]
  className?: string
}

interface ProcessingResult {
  file: File
  status: 'processing' | 'completed' | 'error'
  progress: number
  message?: string
  documentId?: string
}

const getFileIcon = (fileType: string) => {
  if (fileType.includes('pdf')) return <FileText className="h-8 w-8 text-red-500" />
  if (fileType.includes('image')) return <FileImage className="h-8 w-8 text-green-500" />
  if (fileType.includes('spreadsheet') || fileType.includes('excel')) return <FileSpreadsheet className="h-8 w-8 text-green-600" />
  if (fileType.includes('word') || fileType.includes('document')) return <FileText className="h-8 w-8 text-blue-500" />
  return <File className="h-8 w-8 text-gray-500" />
}

const getFileTypeLabel = (fileType: string) => {
  if (fileType.includes('pdf')) return 'PDF'
  if (fileType.includes('image')) return 'Image'
  if (fileType.includes('spreadsheet') || fileType.includes('excel')) return 'Spreadsheet'
  if (fileType.includes('word') || fileType.includes('document')) return 'Document'
  return 'File'
}

export function DocumentUpload({
  onUpload,
  onProcessingComplete,
  maxFiles = 10,
  maxSize = 50 * 1024 * 1024, // 50MB
  acceptedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain',
    'text/markdown',
    'image/jpeg',
    'image/png',
    'image/gif'
  ],
  className
}: DocumentUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<ProcessingResult[]>([])
  const [isProcessing, setIsProcessing] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const newFiles: ProcessingResult[] = acceptedFiles.map(file => ({
      file,
      status: 'processing',
      progress: 0
    }))

    setUploadedFiles(prev => [...prev, ...newFiles])
    setIsProcessing(true)

    // Simulate file processing
    for (let i = 0; i < newFiles.length; i++) {
      const file = newFiles[i]
      
      // Simulate progress updates
      for (let progress = 0; progress <= 100; progress += 10) {
        await new Promise(resolve => setTimeout(resolve, 100))
        setUploadedFiles(prev => 
          prev.map(f => 
            f.file === file.file 
              ? { ...f, progress }
              : f
          )
        )
      }

      // Simulate completion
      setUploadedFiles(prev => 
        prev.map(f => 
          f.file === file.file 
            ? { 
                ...f, 
                status: 'completed', 
                progress: 100,
                documentId: `doc_${Date.now()}_${i}`,
                message: 'Document processed successfully'
              }
            : f
        )
      )
    }

    setIsProcessing(false)
    onUpload?.(acceptedFiles)
    onProcessingComplete?.(newFiles)
  }, [onUpload, onProcessingComplete])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    maxFiles,
    maxSize,
    accept: acceptedTypes.reduce((acc, type) => ({ ...acc, [type]: [] }), {}),
    onDropRejected: (rejectedFiles) => {
      console.log('Rejected files:', rejectedFiles)
    }
  })

  const removeFile = (fileToRemove: File) => {
    setUploadedFiles(prev => prev.filter(f => f.file !== fileToRemove))
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      case 'processing':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
      default:
        return <File className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'error':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'processing':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* Upload Area */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Document Upload
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div
            {...getRootProps()}
            className={cn(
              'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
              isDragActive && !isDragReject && 'border-blue-500 bg-blue-50',
              isDragReject && 'border-red-500 bg-red-50',
              !isDragActive && 'border-gray-300 hover:border-gray-400'
            )}
          >
            <input {...getInputProps()} />
            <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <p className="text-lg font-medium text-gray-900 mb-2">
              {isDragActive 
                ? isDragReject 
                  ? 'File type not supported' 
                  : 'Drop files here'
                : 'Drag & drop documents here'
              }
            </p>
            <p className="text-sm text-gray-500 mb-4">
              or click to browse files
            </p>
            <div className="flex flex-wrap gap-2 justify-center">
              {acceptedTypes.map(type => (
                <Badge key={type} variant="outline" className="text-xs">
                  {getFileTypeLabel(type)}
                </Badge>
              ))}
            </div>
            <p className="text-xs text-gray-400 mt-2">
              Max {maxFiles} files, {Math.round(maxSize / 1024 / 1024)}MB each
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Uploaded Documents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {uploadedFiles.map((result, index) => (
                <div
                  key={`${result.file.name}-${index}`}
                  className="flex items-center justify-between p-3 border rounded-lg"
                >
                  <div className="flex items-center gap-3 flex-1">
                    {getFileIcon(result.file.type)}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">
                        {result.file.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {(result.file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(result.status)}
                      <Badge 
                        variant="outline" 
                        className={cn('text-xs', getStatusColor(result.status))}
                      >
                        {result.status}
                      </Badge>
                    </div>
                    
                    {result.status === 'processing' && (
                      <div className="w-20">
                        <Progress value={result.progress} className="h-2" />
                      </div>
                    )}
                    
                    {result.status === 'completed' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(result.file)}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              ))}
            </div>
            
            {isProcessing && (
              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
                  <span className="text-sm text-blue-700">
                    Processing documents...
                  </span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
