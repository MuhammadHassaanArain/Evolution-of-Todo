'use client'

import { useAuth } from '@/contexts/auth'

export default function ProfilePage() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
   
      {/* Main content */}
      <main className="py-10">
        <div className="max-w-3xl mx-auto sm:px-6 lg:px-8">
          <div className="bg-white shadow-lg rounded-xl overflow-hidden">
            {/* Header */}
            <div className="px-6 py-5 border-b border-gray-200">
              <h3 className="text-xl font-semibold text-gray-900">User Profile</h3>
              <p className="mt-1 text-sm text-gray-500">Personal information and account settings</p>
            </div>

            {/* Profile details */}
            <div className="px-6 py-6 sm:p-8">
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div className="bg-gray-50 p-4 rounded-lg shadow-sm">
                  <label className="block text-sm font-medium text-gray-700">Full Name</label>
                  <div className="mt-1 text-gray-900 text-sm">
                    {user?.first_name && user?.last_name
                      ? `${user.first_name} ${user.last_name}`
                      : user?.username || user?.email || 'User'}
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg shadow-sm">
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <div className="mt-1 text-gray-900 text-sm">{user?.email || 'Not provided'}</div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg shadow-sm">
                  <label className="block text-sm font-medium text-gray-700">Username</label>
                  <div className="mt-1 text-gray-900 text-sm">{user?.username || 'Not provided'}</div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg shadow-sm">
                  <label className="block text-sm font-medium text-gray-700">Member since</label>
                  <div className="mt-1 text-gray-900 text-sm">
                    {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Unknown'}
                  </div>
                </div>
              </div>
            </div>

            {/* Optional: CTA or footer inside card */}
            <div className="px-6 py-4 border-t border-gray-200 text-center">
              <p className="text-sm text-gray-500">
                Manage your account settings and preferences here.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
