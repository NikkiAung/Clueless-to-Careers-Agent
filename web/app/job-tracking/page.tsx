"use client";

import { motion } from "framer-motion";
import {
  Briefcase,
  Plus,
  Search,
  Filter,
  Building2,
  MapPin,
  Calendar,
  ExternalLink,
  MoreHorizontal,
  Clock,
  CheckCircle2,
  XCircle,
  MessageSquare,
  Sparkles,
} from "lucide-react";
import { useState } from "react";

// Mock job applications data
const mockJobs = [
  {
    id: 1,
    company: "Google",
    position: "Software Engineer",
    location: "Mountain View, CA",
    salary: "$150k - $200k",
    status: "applied",
    appliedDate: "2024-12-01",
    logo: "G",
    color: "from-blue-500 to-green-500",
  },
  {
    id: 2,
    company: "Meta",
    position: "Frontend Developer",
    location: "Menlo Park, CA",
    salary: "$140k - $180k",
    status: "interview",
    appliedDate: "2024-11-28",
    logo: "M",
    color: "from-blue-600 to-purple-600",
  },
  {
    id: 3,
    company: "Apple",
    position: "iOS Developer",
    location: "Cupertino, CA",
    salary: "$160k - $210k",
    status: "offer",
    appliedDate: "2024-11-20",
    logo: "A",
    color: "from-slate-600 to-slate-800",
  },
  {
    id: 4,
    company: "Netflix",
    position: "Full Stack Engineer",
    location: "Los Gatos, CA",
    salary: "$170k - $220k",
    status: "rejected",
    appliedDate: "2024-11-15",
    logo: "N",
    color: "from-red-600 to-red-800",
  },
  {
    id: 5,
    company: "Stripe",
    position: "Backend Engineer",
    location: "San Francisco, CA",
    salary: "$155k - $195k",
    status: "applied",
    appliedDate: "2024-12-03",
    logo: "S",
    color: "from-purple-500 to-indigo-600",
  },
];

const statusConfig = {
  applied: {
    label: "Applied",
    icon: Clock,
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
    border: "border-cyan-500/20",
  },
  interview: {
    label: "Interview",
    icon: MessageSquare,
    color: "text-yellow-400",
    bg: "bg-yellow-500/10",
    border: "border-yellow-500/20",
  },
  offer: {
    label: "Offer",
    icon: CheckCircle2,
    color: "text-green-400",
    bg: "bg-green-500/10",
    border: "border-green-500/20",
  },
  rejected: {
    label: "Rejected",
    icon: XCircle,
    color: "text-red-400",
    bg: "bg-red-500/10",
    border: "border-red-500/20",
  },
};

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export default function JobTrackingPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedFilter, setSelectedFilter] = useState<string | null>(null);

  const filteredJobs = mockJobs.filter((job) => {
    const matchesSearch =
      job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.position.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = selectedFilter ? job.status === selectedFilter : true;
    return matchesSearch && matchesFilter;
  });

  const stats = {
    total: mockJobs.length,
    applied: mockJobs.filter((j) => j.status === "applied").length,
    interview: mockJobs.filter((j) => j.status === "interview").length,
    offer: mockJobs.filter((j) => j.status === "offer").length,
  };

  return (
    <div className="min-h-screen bg-slate-950 pt-24 pb-12">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/3 -right-1/4 w-1/2 h-1/2 bg-purple-500/10 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-1/3 -left-1/4 w-1/2 h-1/2 bg-cyan-500/10 rounded-full blur-[120px] animate-pulse delay-1000" />
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-7xl mx-auto px-6 relative z-10"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-orange-500/10 border border-purple-500/20 mb-6"
          >
            <Sparkles className="w-4 h-4 text-purple-400" />
            <span className="text-sm text-purple-300">Track Your Applications</span>
          </motion.div>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent">
                Job Tracking
              </h1>
              <p className="text-slate-400 mt-2">
                Manage and track all your job applications in one place
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 px-5 py-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl text-white font-medium shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 transition-all duration-300"
            >
              <Plus className="w-5 h-5" />
              Add Application
            </motion.button>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          variants={itemVariants}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
        >
          {[
            { label: "Total", value: stats.total, color: "from-slate-500 to-slate-700" },
            { label: "Applied", value: stats.applied, color: "from-cyan-500 to-blue-500" },
            { label: "Interview", value: stats.interview, color: "from-yellow-500 to-orange-500" },
            { label: "Offers", value: stats.offer, color: "from-green-500 to-emerald-500" },
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
              className="relative overflow-hidden bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800 group"
            >
              <div
                className={`absolute inset-0 bg-gradient-to-br ${stat.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}
              />
              <p className="text-slate-400 text-sm">{stat.label}</p>
              <p className="text-3xl font-bold text-white mt-1">{stat.value}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Search and Filter */}
        <motion.div
          variants={itemVariants}
          className="flex flex-col md:flex-row gap-4 mb-6"
        >
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
            <input
              type="text"
              placeholder="Search companies or positions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-slate-900/50 border border-slate-800 rounded-xl text-white placeholder:text-slate-500 focus:outline-none focus:border-purple-500/50 focus:ring-2 focus:ring-purple-500/20 transition-all duration-300"
            />
          </div>
          <div className="flex gap-2">
            {Object.entries(statusConfig).map(([key, config]) => {
              const Icon = config.icon;
              return (
                <motion.button
                  key={key}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() =>
                    setSelectedFilter(selectedFilter === key ? null : key)
                  }
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all duration-300 ${
                    selectedFilter === key
                      ? `${config.bg} ${config.border} ${config.color}`
                      : "bg-slate-900/50 border-slate-800 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden md:inline text-sm">{config.label}</span>
                </motion.button>
              );
            })}
          </div>
        </motion.div>

        {/* Job List */}
        <motion.div variants={containerVariants} className="space-y-4">
          {filteredJobs.map((job, index) => {
            const status = statusConfig[job.status as keyof typeof statusConfig];
            const StatusIcon = status.icon;

            return (
              <motion.div
                key={job.id}
                variants={itemVariants}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ scale: 1.01, x: 5 }}
                className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800 hover:border-purple-500/30 transition-all duration-300 group"
              >
                <div className="flex flex-col md:flex-row md:items-center gap-4">
                  {/* Company Logo */}
                  <div
                    className={`w-14 h-14 rounded-xl bg-gradient-to-br ${job.color} flex items-center justify-center text-white text-xl font-bold shrink-0`}
                  >
                    {job.logo}
                  </div>

                  {/* Job Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="text-lg font-semibold text-white group-hover:text-purple-300 transition-colors">
                          {job.position}
                        </h3>
                        <div className="flex flex-wrap items-center gap-3 mt-1 text-sm text-slate-400">
                          <span className="flex items-center gap-1">
                            <Building2 className="w-3.5 h-3.5" />
                            {job.company}
                          </span>
                          <span className="flex items-center gap-1">
                            <MapPin className="w-3.5 h-3.5" />
                            {job.location}
                          </span>
                          <span className="text-emerald-400">{job.salary}</span>
                        </div>
                      </div>

                      {/* Status Badge */}
                      <div
                        className={`flex items-center gap-2 px-3 py-1.5 rounded-full ${status.bg} ${status.border} border`}
                      >
                        <StatusIcon className={`w-4 h-4 ${status.color}`} />
                        <span className={`text-sm font-medium ${status.color}`}>
                          {status.label}
                        </span>
                      </div>
                    </div>

                    {/* Applied Date and Actions */}
                    <div className="flex items-center justify-between mt-4">
                      <span className="flex items-center gap-1 text-sm text-slate-500">
                        <Calendar className="w-3.5 h-3.5" />
                        Applied {new Date(job.appliedDate).toLocaleDateString()}
                      </span>
                      <div className="flex items-center gap-2">
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          className="p-2 rounded-lg bg-slate-800/50 text-slate-400 hover:text-white hover:bg-slate-800 transition-all duration-200"
                        >
                          <ExternalLink className="w-4 h-4" />
                        </motion.button>
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          className="p-2 rounded-lg bg-slate-800/50 text-slate-400 hover:text-white hover:bg-slate-800 transition-all duration-200"
                        >
                          <MoreHorizontal className="w-4 h-4" />
                        </motion.button>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Empty State */}
        {filteredJobs.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center py-16 bg-slate-900/30 rounded-2xl border border-slate-800 border-dashed"
          >
            <Briefcase className="w-16 h-16 text-slate-600" />
            <h3 className="text-slate-400 text-lg font-medium mt-4">
              No applications found
            </h3>
            <p className="text-slate-500 text-sm mt-2">
              Try adjusting your search or filters
            </p>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}


