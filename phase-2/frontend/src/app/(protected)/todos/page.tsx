'use client';

import { useState } from 'react';
import TaskList from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function TodosPage() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTaskCreated = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main>
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <Card>
              <CardHeader>
                <CardTitle>Todo Management</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <TaskForm onTaskCreated={handleTaskCreated} />
                <TaskList key={refreshTrigger} />
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}