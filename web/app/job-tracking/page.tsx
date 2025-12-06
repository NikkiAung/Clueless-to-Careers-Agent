"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  Briefcase,
  Plus,
  Search,
  Building2,
  MapPin,
  Calendar,
  ExternalLink,
  MoreHorizontal,
  Clock,
  CheckCircle2,
  XCircle,
  MessageSquare,
  FileText,
  Link as LinkIcon,
  ChevronDown,
  Download,
  Eye,
  X,
} from "lucide-react";
import { useState } from "react";

// Mock job applications data with job links and resume info
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
    jobUrl: "https://careers.google.com/jobs/results/123456789",
    resumeUsed: {
      name: "Resume_SWE_v3.pdf",
      uploadedAt: "2024-11-30",
      size: "245 KB",
    },
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
    jobUrl: "https://metacareers.com/jobs/456789123",
    resumeUsed: {
      name: "Resume_Frontend_v2.pdf",
      uploadedAt: "2024-11-27",
      size: "198 KB",
    },
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
    jobUrl: "https://jobs.apple.com/en-us/details/200012345",
    resumeUsed: {
      name: "Resume_iOS_v4.pdf",
      uploadedAt: "2024-11-19",
      size: "312 KB",
    },
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
    jobUrl: "https://jobs.netflix.com/jobs/987654321",
    resumeUsed: {
      name: "Resume_FullStack_v1.pdf",
      uploadedAt: "2024-11-14",
      size: "267 KB",
    },
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
    jobUrl: "https://stripe.com/jobs/listing/backend-engineer/5678912",
    resumeUsed: {
      name: "Resume_Backend_v2.pdf",
      uploadedAt: "2024-12-02",
      size: "223 KB",
    },
  },
];

const statusConfig = {
  applied: {
    label: "Applied",
    icon: Clock,
    color: "text-neutral-300",
    bg: "bg-white/5",
    border: "border-white/10",
  },
  interview: {
    label: "Interview",
    icon: MessageSquare,
    color: "text-white",
    bg: "bg-white/10",
    border: "border-white/20",
  },
  offer: {
    label: "Offer",
    icon: CheckCircle2,
    color: "text-white",
    bg: "bg-white/15",
    border: "border-white/30",
  },
  rejected: {
    label: "Rejected",
    icon: XCircle,
    color: "text-neutral-500",
    bg: "bg-white/[0.02]",
    border: "border-white/5",
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
  const [expandedJob, setExpandedJob] = useState<number | null>(null);
  const [resumePreview, setResumePreview] = useState<{
    name: string;
    company: string;
  } | null>(null);

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
    <div className="min-h-screen bg-black pt-24 pb-12">
      {/* Subtle Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/3 -right-1/4 w-1/2 h-1/2 bg-white/[0.01] rounded-full blur-[120px]" />
        <div className="absolute bottom-1/3 -left-1/4 w-1/2 h-1/2 bg-white/[0.01] rounded-full blur-[120px]" />
      </div>

      {/* Resume Preview Modal */}
      <AnimatePresence>
        {resumePreview && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
            onClick={() => setResumePreview(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-neutral-900 rounded-2xl border border-white/10 w-full max-w-2xl max-h-[80vh] overflow-hidden"
            >
              {/* Modal Header */}
              <div className="flex items-center justify-between p-6 border-b border-white/10">
                <div>
                  <h3 className="text-lg font-semibold text-white">
                    Resume Preview
                  </h3>
                  <p className="text-sm text-neutral-500 mt-1">
                    Used for {resumePreview.company} application
                  </p>
                </div>
                <button
                  onClick={() => setResumePreview(null)}
                  className="p-2 rounded-lg bg-white/5 text-neutral-400 hover:text-white hover:bg-white/10 transition-all"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Modal Content - Resume Preview */}
              <div className="p-6">
                <div className="bg-white/[0.02] rounded-xl border border-white/10 p-8 min-h-[400px] flex flex-col items-center justify-center">
                  <FileText className="w-16 h-16 text-neutral-600 mb-4" />
                  <p className="text-white font-medium">{resumePreview.name}</p>
                  <p className="text-neutral-500 text-sm mt-2">
                    PDF Document Preview
                  </p>
                  <div className="flex gap-3 mt-6">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="flex items-center gap-2 px-4 py-2 bg-white rounded-lg text-black font-medium text-sm hover:bg-neutral-200 transition-all"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-lg text-white font-medium text-sm hover:bg-white/20 transition-all"
                    >
                      <Eye className="w-4 h-4" />
                      Open in New Tab
                    </motion.button>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

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
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-6"
          >
            <div className="w-2 h-2 rounded-full bg-white" />
            <span className="text-sm text-neutral-400">
              Track Your Applications
            </span>
          </motion.div>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold text-white tracking-tight">
                Job Tracking
              </h1>
              <p className="text-neutral-500 mt-2">
                Manage and track all your job applications in one place
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 px-5 py-3 bg-white rounded-xl text-black font-medium hover:bg-neutral-200 transition-all duration-300"
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
            { label: "Total", value: stats.total },
            { label: "Applied", value: stats.applied },
            { label: "Interview", value: stats.interview },
            { label: "Offers", value: stats.offer },
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
              className="relative overflow-hidden bg-white/[0.02] backdrop-blur-sm rounded-2xl p-6 border border-white/10 group hover:border-white/20 transition-all duration-300"
            >
              <p className="text-neutral-500 text-sm">{stat.label}</p>
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
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
            <input
              type="text"
              placeholder="Search companies or positions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-white/[0.02] border border-white/10 rounded-xl text-white placeholder:text-neutral-600 focus:outline-none focus:border-white/30 focus:ring-1 focus:ring-white/10 transition-all duration-300"
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
                      ? "bg-white text-black border-white"
                      : "bg-white/[0.02] border-white/10 text-neutral-400 hover:border-white/20"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden md:inline text-sm">
                    {config.label}
                  </span>
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
            const isExpanded = expandedJob === job.id;

            return (
              <motion.div
                key={job.id}
                variants={itemVariants}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-white/[0.02] backdrop-blur-sm rounded-2xl border border-white/10 hover:border-white/20 transition-all duration-300 group overflow-hidden"
              >
                {/* Main Job Card */}
                <div className="p-6">
                  <div className="flex flex-col md:flex-row md:items-center gap-4">
                    {/* Company Logo */}
                    <div className="w-14 h-14 rounded-xl bg-white flex items-center justify-center text-black text-xl font-bold shrink-0">
                      {job.logo}
                    </div>

                    {/* Job Details */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <h3 className="text-lg font-semibold text-white group-hover:text-neutral-200 transition-colors">
                            {job.position}
                          </h3>
                          <div className="flex flex-wrap items-center gap-3 mt-1 text-sm text-neutral-500">
                            <span className="flex items-center gap-1">
                              <Building2 className="w-3.5 h-3.5" />
                              {job.company}
                            </span>
                            <span className="flex items-center gap-1">
                              <MapPin className="w-3.5 h-3.5" />
                              {job.location}
                            </span>
                            <span className="text-neutral-400">{job.salary}</span>
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
                        <span className="flex items-center gap-1 text-sm text-neutral-600">
                          <Calendar className="w-3.5 h-3.5" />
                          Applied{" "}
                          {new Date(job.appliedDate).toLocaleDateString()}
                        </span>
                        <div className="flex items-center gap-2">
                          {/* Job Link Button */}
                          <motion.a
                            href={job.jobUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="p-2 rounded-lg bg-white/5 text-neutral-500 hover:text-white hover:bg-white/10 transition-all duration-200"
                            title="View Job Posting"
                          >
                            <ExternalLink className="w-4 h-4" />
                          </motion.a>
                          {/* Expand Button */}
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            onClick={() =>
                              setExpandedJob(isExpanded ? null : job.id)
                            }
                            className="p-2 rounded-lg bg-white/5 text-neutral-500 hover:text-white hover:bg-white/10 transition-all duration-200"
                          >
                            <motion.div
                              animate={{ rotate: isExpanded ? 180 : 0 }}
                              transition={{ duration: 0.2 }}
                            >
                              <ChevronDown className="w-4 h-4" />
                            </motion.div>
                          </motion.button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Expanded Details */}
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="overflow-hidden"
                    >
                      <div className="px-6 pb-6 pt-2 border-t border-white/5">
                        <div className="grid md:grid-cols-2 gap-4">
                          {/* Job Link Section */}
                          <div className="bg-white/[0.02] rounded-xl p-4 border border-white/5">
                            <div className="flex items-center gap-2 mb-3">
                              <LinkIcon className="w-4 h-4 text-neutral-400" />
                              <span className="text-sm font-medium text-white">
                                Job Posting
                              </span>
                            </div>
                            <a
                              href={job.jobUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-neutral-400 hover:text-white transition-colors break-all flex items-start gap-2 group/link"
                            >
                              <span className="truncate">{job.jobUrl}</span>
                              <ExternalLink className="w-3.5 h-3.5 shrink-0 opacity-0 group-hover/link:opacity-100 transition-opacity" />
                            </a>
                            <motion.a
                              href={job.jobUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              whileHover={{ scale: 1.02 }}
                              whileTap={{ scale: 0.98 }}
                              className="mt-3 inline-flex items-center gap-2 px-3 py-1.5 bg-white/10 rounded-lg text-sm text-white hover:bg-white/20 transition-all"
                            >
                              <ExternalLink className="w-3.5 h-3.5" />
                              Open Job Posting
                            </motion.a>
                          </div>

                          {/* Resume Section */}
                          <div className="bg-white/[0.02] rounded-xl p-4 border border-white/5">
                            <div className="flex items-center gap-2 mb-3">
                              <FileText className="w-4 h-4 text-neutral-400" />
                              <span className="text-sm font-medium text-white">
                                Resume Used
                              </span>
                            </div>
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-12 bg-white/10 rounded-lg flex items-center justify-center">
                                <FileText className="w-5 h-5 text-neutral-400" />
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm text-white font-medium truncate">
                                  {job.resumeUsed.name}
                                </p>
                                <p className="text-xs text-neutral-500 mt-0.5">
                                  {job.resumeUsed.size} • Uploaded{" "}
                                  {new Date(
                                    job.resumeUsed.uploadedAt
                                  ).toLocaleDateString()}
                                </p>
                              </div>
                            </div>
                            <div className="flex gap-2 mt-3">
                              <motion.button
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() =>
                                  setResumePreview({
                                    name: job.resumeUsed.name,
                                    company: job.company,
                                  })
                                }
                                className="flex-1 inline-flex items-center justify-center gap-2 px-3 py-1.5 bg-white rounded-lg text-sm text-black font-medium hover:bg-neutral-200 transition-all"
                              >
                                <Eye className="w-3.5 h-3.5" />
                                View Resume
                              </motion.button>
                              <motion.button
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                className="inline-flex items-center justify-center gap-2 px-3 py-1.5 bg-white/10 rounded-lg text-sm text-white hover:bg-white/20 transition-all"
                              >
                                <Download className="w-3.5 h-3.5" />
                              </motion.button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Empty State */}
        {filteredJobs.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center py-16 bg-white/[0.02] rounded-2xl border border-white/10 border-dashed"
          >
            <Briefcase className="w-16 h-16 text-neutral-600" />
            <h3 className="text-neutral-400 text-lg font-medium mt-4">
              No applications found
            </h3>
            <p className="text-neutral-600 text-sm mt-2">
              Try adjusting your search or filters
            </p>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
