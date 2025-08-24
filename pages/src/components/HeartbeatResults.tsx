import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Heart, AlertTriangle, CheckCircle, Activity, Info, Download } from 'lucide-react';

export interface HeartbeatResult {
  condition: 'artifact' | 'extrasystole' | 'murmur' | 'normal';
  confidence: number;
  timestamp: string;
}

interface HeartbeatResultsProps {
  result: HeartbeatResult;
}

export const HeartbeatResults: React.FC<HeartbeatResultsProps> = ({ result }) => {
  const getConditionDetails = (condition: HeartbeatResult['condition']) => {
    switch (condition) {
      case 'normal':
        return {
          title: 'Normal Heart Rhythm',
          description: 'No abnormal patterns detected in the heartbeat recording',
          severity: 'low',
          icon: CheckCircle,
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          recommendations: [
            'Continue maintaining a healthy lifestyle',
            'Regular exercise and balanced diet',
            'Keep up with routine cardiac checkups'
          ]
        };
      case 'murmur':
        return {
          title: 'Heart Murmur Detected',
          description: 'Unusual heart sounds that may indicate turbulent blood flow',
          severity: 'medium',
          icon: Heart,
          color: 'text-orange-600',
          bgColor: 'bg-orange-50',
          recommendations: [
            'Consult a cardiologist for detailed evaluation',
            'Consider echocardiogram for structural assessment',
            'Monitor symptoms like chest pain or shortness of breath'
          ]
        };
      case 'extrasystole':
        return {
          title: 'Extrasystole (Premature Beats)',
          description: 'Extra heartbeats that occur earlier than expected',
          severity: 'medium',
          icon: Activity,
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-50',
          recommendations: [
            'Monitor frequency and triggers of irregular beats',
            'Consider Holter monitoring for 24-hour assessment',
            'Avoid excessive caffeine and stress'
          ]
        };
      case 'artifact':
        return {
          title: 'Recording Artifact',
          description: 'Audio quality issues detected - may affect analysis accuracy',
          severity: 'low',
          icon: AlertTriangle,
          color: 'text-gray-600',
          bgColor: 'bg-gray-50',
          recommendations: [
            'Record in a quieter environment',
            'Ensure proper microphone placement',
            'Try recording again with better audio quality'
          ]
        };
      default:
        return {
          title: 'Unknown Condition',
          description: 'Unable to classify the heart sound pattern',
          severity: 'medium',
          icon: Info,
          color: 'text-gray-600',
          bgColor: 'bg-gray-50',
          recommendations: [
            'Consult a healthcare professional',
            'Consider professional cardiac examination'
          ]
        };
    }
  };

  const conditionInfo = getConditionDetails(result.condition);
  const IconComponent = conditionInfo.icon;
  const confidencePercentage = Math.round(result.confidence * 100);
  
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'low':
        return <Badge variant="outline" className="text-green-600 border-green-200">Low Priority</Badge>;
      case 'medium':
        return <Badge variant="outline" className="text-orange-600 border-orange-200">Moderate Priority</Badge>;
      case 'high':
        return <Badge variant="destructive">High Priority</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Main Result Card */}
      <Card className="bg-gradient-card shadow-elegant border-medical-accent/20">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className={`p-3 rounded-full ${conditionInfo.bgColor}`}>
                <IconComponent className={`h-8 w-8 ${conditionInfo.color}`} />
              </div>
              <div>
                <CardTitle className="text-2xl text-medical-primary">{conditionInfo.title}</CardTitle>
                <CardDescription className="text-lg mt-2">
                  {conditionInfo.description}
                </CardDescription>
              </div>
            </div>
            {getSeverityBadge(conditionInfo.severity)}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground">Confidence Score</p>
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-muted rounded-full h-2">
                  <div 
                    className="bg-medical-primary h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${confidencePercentage}%` }}
                  />
                </div>
                <span className="text-lg font-bold text-medical-primary">{confidencePercentage}%</span>
              </div>
            </div>
            <div className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground">Analysis Time</p>
              <p className="text-sm text-foreground">
                {new Date(result.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recommendations */}
      <Card className="bg-gradient-card shadow-soft border-medical-accent/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-medical-primary">
            <Heart className="h-5 w-5" />
            Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {conditionInfo.recommendations.map((recommendation, index) => (
              <li key={index} className="flex items-start gap-3">
                <div className="w-2 h-2 bg-medical-primary rounded-full mt-2 flex-shrink-0" />
                <span className="text-muted-foreground">{recommendation}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Medical Disclaimer */}
      <Alert className="border-medical-accent/20 bg-medical-accent/5">
        <AlertTriangle className="h-4 w-4" />
        <AlertTitle>Important Medical Disclaimer</AlertTitle>
        <AlertDescription className="mt-2 space-y-2">
          <p>
            This AI analysis is for preliminary assessment only and should not replace professional medical diagnosis. 
            Always consult with a qualified cardiologist or healthcare provider for proper evaluation and treatment.
          </p>
          <p className="font-medium">
            If you experience chest pain, shortness of breath, or other cardiac symptoms, seek immediate medical attention.
          </p>
        </AlertDescription>
      </Alert>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-4 justify-center">
        <Button variant="outline" size="lg">
          <Download className="h-5 w-5 mr-2" />
          Download Report
        </Button>
        <Button variant="medical" size="lg">
          <Heart className="h-5 w-5 mr-2" />
          Analyze Another Recording
        </Button>
      </div>
    </div>
  );
};