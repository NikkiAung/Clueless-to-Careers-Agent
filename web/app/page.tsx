"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Briefcase, User, Zap, Target, TrendingUp } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-black pt-20">
      {/* Subtle Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-white/[0.02] rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-white/[0.02] rounded-full blur-[120px]" />
        
        {/* Grid pattern */}
        <div 
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `linear-gradient(rgba(255,255,255,.1) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(255,255,255,.1) 1px, transparent 1px)`,
            backgroundSize: '60px 60px'
          }}
        />
      </div>

      {/* Hero Section */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          {/* Badge */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8"
          >
            <div className="w-2 h-2 rounded-full bg-white animate-pulse" />
            <span className="text-sm text-neutral-400">Your Career Companion</span>
          </motion.div>

          {/* Main Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-5xl md:text-7xl font-bold mb-6 tracking-tight"
          >
            <span className="text-white">Launch Your</span>
            <br />
            <span className="text-white">Dream Career</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl text-neutral-500 max-w-2xl mx-auto mb-12"
          >
            Build a stunning portfolio, track your applications, and land your dream job with our intelligent career management platform.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link href="/profile">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="group flex items-center gap-2 px-8 py-4 bg-white rounded-full text-black font-semibold text-lg transition-all duration-300 hover:bg-neutral-200"
              >
                <User className="w-5 h-5" />
                Build Your Profile
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </motion.button>
            </Link>
            <Link href="/job-tracking">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center gap-2 px-8 py-4 bg-transparent border border-white/20 rounded-full text-white font-semibold text-lg hover:bg-white/5 transition-all duration-300"
              >
                <Briefcase className="w-5 h-5" />
                Track Applications
              </motion.button>
            </Link>
          </motion.div>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="relative z-20 grid md:grid-cols-3 gap-6 mt-24"
        >
          {[
            {
              icon: Zap,
              title: "Smart Resume Parsing",
              description: "Upload your resume and let AI extract your skills, experience, and projects automatically.",
            },
            {
              icon: Target,
              title: "Job Application Tracker",
              description: "Keep track of all your applications, interviews, and offers in one organized dashboard.",
            },
            {
              icon: TrendingUp,
              title: "Career Insights",
              description: "Get personalized recommendations and insights to improve your job search success.",
            },
          ].map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 + index * 0.1 }}
              whileHover={{ scale: 1.03, y: -5 }}
              className="relative group"
            >
              <div className="relative bg-white/[0.02] backdrop-blur-sm rounded-2xl p-8 border border-white/10 group-hover:border-white/20 transition-all duration-300">
                <div className="inline-flex p-3 rounded-xl bg-white/10 mb-4">
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-neutral-500">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Floating elements */}
        <div className="absolute top-32 left-10 hidden lg:block z-0">
          <motion.div
            animate={{ y: [0, -20, 0], rotate: [0, 5, 0] }}
            transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
            className="w-20 h-20 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-sm"
          />
        </div>
        <div className="absolute top-48 right-16 hidden lg:block z-0">
          <motion.div
            animate={{ y: [0, 20, 0], rotate: [0, -5, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
            className="w-16 h-16 rounded-full bg-white/[0.03] border border-white/10 backdrop-blur-sm"
          />
        </div>
        <div className="absolute bottom-32 left-20 hidden lg:block z-0">
          <motion.div
            animate={{ y: [0, 15, 0], x: [0, 10, 0] }}
            transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
            className="w-12 h-12 rounded-xl bg-white/[0.03] border border-white/10 backdrop-blur-sm"
          />
        </div>
      </div>
    </div>
  );
}
