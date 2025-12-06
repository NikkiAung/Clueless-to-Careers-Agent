"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useCallback } from "react";
import {
  User,
  GraduationCap,
  Upload,
  Code2,
  Briefcase,
  FolderGit2,
  Calendar,
  MapPin,
  Building2,
  FileText,
  CheckCircle2,
  Plus,
  ChevronDown,
} from "lucide-react";

// Mock data for demonstration
const mockResumeData = {
  technicalSkills: [
    "Python",
    "JavaScript",
    "TypeScript",
    "React",
    "Next.js",
    "Node.js",
    "PostgreSQL",
    "MongoDB",
    "Docker",
    "AWS",
    "Git",
    "TailwindCSS",
  ],
  experience: [
    {
      title: "Computer Science Tutor",
      company: "City College of San Francisco",
      location: "San Francisco, CA",
      period: "Aug 2024 - Present",
      duration: "1 yr 5 mos",
      description: ["Computer Science Tutor Squad", "CS 110A, CS 111B"],
      type: "Part-time",
    },
    {
      title: "Computer Science Teaching Assistant",
      company: "City College of San Francisco",
      location: "San Francisco, CA",
      period: "Aug 2024 - Present",
      duration: "1 yr 5 mos",
      description: ["Office hours and grading"],
      type: "Part-time",
    },
    {
      title: "Software Engineering Fellow",
      company: "Headstarter AI",
      location: "Remote",
      period: "Jul 2024 - Sep 2024",
      duration: "3 mos",
      description: [],
      type: "Fellowship",
    },
    {
      title: "Build Projects Fellow",
      company: "The Build Fellowship by Open Avenues",
      location: "Remote",
      period: "Apr 2024 - Jun 2024",
      duration: "3 mos",
      description: [
        "Under the supervision of an industry practitioner, worked on a project to apply industry tools to specific real-world challenges.",
      ],
      skills: ["Full-Stack Development"],
      type: "Fellowship",
    },
  ],
  projects: [
    {
      name: "AI-Powered Resume Builder",
      description:
        "Built a full-stack application using Next.js, TypeScript, and OpenAI API to generate tailored resumes",
      technologies: ["Next.js", "TypeScript", "OpenAI", "TailwindCSS"],
    },
    {
      name: "E-Commerce Platform",
      description:
        "Developed a scalable e-commerce solution with real-time inventory management",
      technologies: ["React", "Node.js", "PostgreSQL", "Stripe"],
    },
    {
      name: "Task Management Dashboard",
      description:
        "Created a collaborative task management tool with real-time updates",
      technologies: ["React", "Firebase", "Material-UI"],
    },
  ],
};

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export default function ProfilePage() {
  const [name, setName] = useState("");
  const [education, setEducation] = useState({
    school: "",
    degree: "",
    startDate: "",
    endDate: "",
  });
  const [resumeUploaded, setResumeUploaded] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [resumeData, setResumeData] = useState<typeof mockResumeData | null>(null);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    processResume();
  }, []);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      processResume();
    }
  };

  const processResume = () => {
    setIsProcessing(true);
    // Simulate processing
    setTimeout(() => {
      setResumeUploaded(true);
      setIsProcessing(false);
      setResumeData(mockResumeData);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-black pt-24 pb-12">
      {/* Subtle Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -left-1/4 w-1/2 h-1/2 bg-white/[0.01] rounded-full blur-[120px]" />
        <div className="absolute bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-white/[0.01] rounded-full blur-[120px]" />
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-6xl mx-auto px-6 relative z-10"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="text-center mb-12">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-6"
          >
            <div className="w-2 h-2 rounded-full bg-white" />
            <span className="text-sm text-neutral-400">Your Career Dashboard</span>
          </motion.div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight">
            Build Your Profile
          </h1>
          <p className="text-neutral-500 text-lg max-w-2xl mx-auto">
            Create a stunning portfolio that showcases your skills and experience
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Personal Info */}
          <motion.div variants={itemVariants} className="lg:col-span-1 space-y-6">
            {/* Name Card */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="bg-white/[0.02] backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-lg bg-white/10">
                  <User className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-lg font-semibold text-white">Your Name</h2>
              </div>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your full name"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder:text-neutral-600 focus:outline-none focus:border-white/30 focus:ring-1 focus:ring-white/10 transition-all duration-300"
              />
            </motion.div>

            {/* Education Card */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="bg-white/[0.02] backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-lg bg-white/10">
                  <GraduationCap className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-lg font-semibold text-white">Education</h2>
              </div>
              <div className="space-y-4">
                <input
                  type="text"
                  value={education.school}
                  onChange={(e) =>
                    setEducation({ ...education, school: e.target.value })
                  }
                  placeholder="School / University"
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder:text-neutral-600 focus:outline-none focus:border-white/30 focus:ring-1 focus:ring-white/10 transition-all duration-300"
                />
                <input
                  type="text"
                  value={education.degree}
                  onChange={(e) =>
                    setEducation({ ...education, degree: e.target.value })
                  }
                  placeholder="Degree / Field of Study"
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder:text-neutral-600 focus:outline-none focus:border-white/30 focus:ring-1 focus:ring-white/10 transition-all duration-300"
                />
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-neutral-500 mb-1 block">
                      Start Date
                    </label>
                    <input
                      type="month"
                      value={education.startDate}
                      onChange={(e) =>
                        setEducation({ ...education, startDate: e.target.value })
                      }
                      className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-white/30 focus:ring-1 focus:ring-white/10 transition-all duration-300 [color-scheme:dark]"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-neutral-500 mb-1 block">
                      End Date
                    </label>
                    <input
                      type="month"
                      value={education.endDate}
                      onChange={(e) =>
                        setEducation({ ...education, endDate: e.target.value })
                      }
                      className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-white/30 focus:ring-1 focus:ring-white/10 transition-all duration-300 [color-scheme:dark]"
                    />
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Resume Upload Card */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="bg-white/[0.02] backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-lg bg-white/10">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-lg font-semibold text-white">Resume</h2>
              </div>

              <motion.label
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`relative flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-300 ${
                  isDragOver
                    ? "border-white bg-white/10"
                    : resumeUploaded
                    ? "border-white/30 bg-white/5"
                    : "border-white/10 hover:border-white/30 bg-white/[0.02]"
                }`}
              >
                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={handleFileUpload}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <AnimatePresence mode="wait">
                  {isProcessing ? (
                    <motion.div
                      key="processing"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      className="flex flex-col items-center"
                    >
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="w-10 h-10 border-2 border-white border-t-transparent rounded-full"
                      />
                      <p className="text-white mt-3 text-sm">
                        Extracting data...
                      </p>
                    </motion.div>
                  ) : resumeUploaded ? (
                    <motion.div
                      key="uploaded"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      className="flex flex-col items-center"
                    >
                      <CheckCircle2 className="w-10 h-10 text-white" />
                      <p className="text-white mt-3 text-sm font-medium">
                        Resume uploaded!
                      </p>
                      <p className="text-neutral-500 text-xs mt-1">
                        Click to replace
                      </p>
                    </motion.div>
                  ) : (
                    <motion.div
                      key="upload"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      className="flex flex-col items-center"
                    >
                      <Upload className="w-10 h-10 text-neutral-500" />
                      <p className="text-neutral-400 mt-3 text-sm">
                        Drop your resume here
                      </p>
                      <p className="text-neutral-600 text-xs mt-1">
                        PDF, DOC, DOCX
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.label>
            </motion.div>
          </motion.div>

          {/* Right Column - Extracted Data */}
          <motion.div variants={itemVariants} className="lg:col-span-2 space-y-6">
            <AnimatePresence>
              {resumeData ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-6"
                >
                  {/* Technical Skills */}
                  <motion.div
                    variants={itemVariants}
                    className="bg-white/[0.02] backdrop-blur-sm rounded-2xl p-6 border border-white/10"
                  >
                    <button
                      onClick={() =>
                        setActiveSection(
                          activeSection === "skills" ? null : "skills"
                        )
                      }
                      className="flex items-center justify-between w-full mb-4"
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-white/10">
                          <Code2 className="w-5 h-5 text-white" />
                        </div>
                        <h2 className="text-lg font-semibold text-white">
                          Technical Skills
                        </h2>
                      </div>
                      <motion.div
                        animate={{ rotate: activeSection === "skills" ? 180 : 0 }}
                      >
                        <ChevronDown className="w-5 h-5 text-neutral-400" />
                      </motion.div>
                    </button>
                    <motion.div
                      initial={false}
                      animate={{
                        height: activeSection === "skills" ? 0 : "auto",
                        opacity: activeSection === "skills" ? 0 : 1,
                      }}
                      className="overflow-hidden"
                    >
                      <div className="flex flex-wrap gap-2">
                        {resumeData.technicalSkills.map((skill, index) => (
                          <motion.span
                            key={skill}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: index * 0.05 }}
                            whileHover={{ scale: 1.1 }}
                            className="px-3 py-1.5 bg-white/5 border border-white/10 rounded-full text-sm text-white hover:bg-white/10 hover:border-white/20 transition-all duration-200"
                          >
                            {skill}
                          </motion.span>
                        ))}
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.95 }}
                          className="px-3 py-1.5 bg-transparent border border-white/10 border-dashed rounded-full text-sm text-neutral-500 hover:border-white/30 hover:text-white transition-all duration-200 flex items-center gap-1"
                        >
                          <Plus className="w-3 h-3" />
                          Add Skill
                        </motion.button>
                      </div>
                    </motion.div>
                  </motion.div>

                  {/* Experience */}
                  <motion.div
                    variants={itemVariants}
                    className="bg-white/[0.02] backdrop-blur-sm rounded-2xl p-6 border border-white/10"
                  >
                    <button
                      onClick={() =>
                        setActiveSection(
                          activeSection === "experience" ? null : "experience"
                        )
                      }
                      className="flex items-center justify-between w-full mb-6"
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-white/10">
                          <Briefcase className="w-5 h-5 text-white" />
                        </div>
                        <h2 className="text-lg font-semibold text-white">
                          Work Experience
                        </h2>
                      </div>
                      <motion.div
                        animate={{
                          rotate: activeSection === "experience" ? 180 : 0,
                        }}
                      >
                        <ChevronDown className="w-5 h-5 text-neutral-400" />
                      </motion.div>
                    </button>
                    <motion.div
                      initial={false}
                      animate={{
                        height: activeSection === "experience" ? 0 : "auto",
                        opacity: activeSection === "experience" ? 0 : 1,
                      }}
                      className="overflow-hidden"
                    >
                      <div className="space-y-6">
                        {resumeData.experience.map((exp, index) => (
                          <motion.div
                            key={index}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="relative pl-6 before:absolute before:left-0 before:top-2 before:w-2 before:h-2 before:rounded-full before:bg-white after:absolute after:left-[3px] after:top-4 after:bottom-0 after:w-0.5 after:bg-white/10 last:after:hidden"
                          >
                            <div className="flex flex-wrap items-start justify-between gap-2 mb-2">
                              <div>
                                <h3 className="text-white font-semibold">
                                  {exp.title}
                                </h3>
                                <div className="flex items-center gap-2 text-neutral-400 text-sm mt-1">
                                  <Building2 className="w-3.5 h-3.5" />
                                  <span>{exp.company}</span>
                                  <span className="text-neutral-600">•</span>
                                  <span className="text-neutral-500">
                                    {exp.type}
                                  </span>
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="flex items-center gap-1 text-neutral-500 text-sm">
                                  <Calendar className="w-3.5 h-3.5" />
                                  <span>{exp.period}</span>
                                </div>
                                <div className="flex items-center gap-1 text-neutral-600 text-xs mt-1">
                                  <MapPin className="w-3 h-3" />
                                  <span>{exp.location}</span>
                                </div>
                              </div>
                            </div>
                            {exp.description.length > 0 && (
                              <ul className="mt-3 space-y-1">
                                {exp.description.map((desc, i) => (
                                  <li
                                    key={i}
                                    className="text-neutral-400 text-sm flex items-start gap-2"
                                  >
                                    <span className="text-white mt-1.5">
                                      •
                                    </span>
                                    {desc}
                                  </li>
                                ))}
                              </ul>
                            )}
                            {exp.skills && (
                              <div className="flex flex-wrap gap-2 mt-3">
                                {exp.skills.map((skill) => (
                                  <span
                                    key={skill}
                                    className="px-2 py-0.5 bg-white/5 border border-white/10 rounded text-xs text-neutral-300"
                                  >
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            )}
                          </motion.div>
                        ))}
                      </div>
                    </motion.div>
                  </motion.div>

                  {/* Projects */}
                  <motion.div
                    variants={itemVariants}
                    className="bg-white/[0.02] backdrop-blur-sm rounded-2xl p-6 border border-white/10"
                  >
                    <button
                      onClick={() =>
                        setActiveSection(
                          activeSection === "projects" ? null : "projects"
                        )
                      }
                      className="flex items-center justify-between w-full mb-6"
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-white/10">
                          <FolderGit2 className="w-5 h-5 text-white" />
                        </div>
                        <h2 className="text-lg font-semibold text-white">
                          Projects
                        </h2>
                      </div>
                      <motion.div
                        animate={{
                          rotate: activeSection === "projects" ? 180 : 0,
                        }}
                      >
                        <ChevronDown className="w-5 h-5 text-neutral-400" />
                      </motion.div>
                    </button>
                    <motion.div
                      initial={false}
                      animate={{
                        height: activeSection === "projects" ? 0 : "auto",
                        opacity: activeSection === "projects" ? 0 : 1,
                      }}
                      className="overflow-hidden"
                    >
                      <div className="grid md:grid-cols-2 gap-4">
                        {resumeData.projects.map((project, index) => (
                          <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ scale: 1.02, y: -5 }}
                            className="p-4 bg-white/[0.02] rounded-xl border border-white/10 hover:border-white/20 transition-all duration-300 group"
                          >
                            <h3 className="text-white font-semibold group-hover:text-neutral-200 transition-colors">
                              {project.name}
                            </h3>
                            <p className="text-neutral-500 text-sm mt-2 line-clamp-2">
                              {project.description}
                            </p>
                            <div className="flex flex-wrap gap-1.5 mt-3">
                              {project.technologies.map((tech) => (
                                <span
                                  key={tech}
                                  className="px-2 py-0.5 bg-white/5 border border-white/10 rounded text-xs text-neutral-400"
                                >
                                  {tech}
                                </span>
                              ))}
                            </div>
                          </motion.div>
                        ))}
                        <motion.button
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          className="p-4 bg-transparent rounded-xl border-2 border-dashed border-white/10 hover:border-white/20 transition-all duration-300 flex flex-col items-center justify-center gap-2 text-neutral-500 hover:text-white min-h-[120px]"
                        >
                          <Plus className="w-6 h-6" />
                          <span className="text-sm">Add Project</span>
                        </motion.button>
                      </div>
                    </motion.div>
                  </motion.div>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center justify-center h-[400px] bg-white/[0.02] rounded-2xl border border-white/10 border-dashed"
                >
                  <motion.div
                    animate={{
                      y: [0, -10, 0],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  >
                    <Upload className="w-16 h-16 text-neutral-600" />
                  </motion.div>
                  <h3 className="text-neutral-400 text-lg font-medium mt-4">
                    Upload your resume
                  </h3>
                  <p className="text-neutral-600 text-sm mt-2 max-w-md text-center">
                    Drop your resume on the left to automatically extract your
                    skills, experience, and projects
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}
