"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { Mail, Lock, User, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";

export default function SignUpPage() {
  const router = useRouter();
  const formRef = useRef<HTMLFormElement>(null);
  
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  // Check if user is already authenticated
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const supabase = createClient();
        const { data: { user } } = await supabase.auth.getUser();
        
        if (user) {
          console.log("User already authenticated, redirecting to profile");
          router.push("/profile");
          router.refresh();
        } else {
          console.log("User not authenticated, showing signup form");
          setIsCheckingAuth(false);
        }
      } catch (err) {
        console.error("Error checking auth:", err);
        setIsCheckingAuth(false);
      }
    };
    
    checkAuth();
  }, [router]);

  const handleSignUp = async (e: React.FormEvent) => {
    if (e && e.preventDefault) {
      e.preventDefault();
    }
    if (e && e.stopPropagation) {
      e.stopPropagation();
    }
    
    console.log("=== Form submission triggered ===", { name, email, loading, passwordLength: password.length });
    
    setError("");

    // Validate form fields
    if (!name.trim()) {
      console.log("Validation failed: Name is required");
      setError("Name is required");
      setLoading(false);
      return;
    }

    if (!email.trim()) {
      console.log("Validation failed: Email is required");
      setError("Email is required");
      setLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      console.log("Validation failed: Passwords do not match");
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      console.log("Validation failed: Password too short");
      setError("Password must be at least 6 characters");
      setLoading(false);
      return;
    }

    console.log("Validation passed, starting signup...");
    setLoading(true);

    try {
      const supabase = createClient();
      const { data, error: signUpError } = await supabase.auth.signUp({
        email: email.trim(),
        password,
        options: {
          data: {
            name: name.trim(),
          },
        },
      });

      if (signUpError) {
        console.error("Sign up error:", signUpError);
        throw signUpError;
      }

      if (data.user) {
        console.log("Signup successful, user created:", data.user.id);
        
        // Wait a moment for the trigger to create the profile, then upsert with name
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Upsert profile with name (will create if doesn't exist, update if it does)
        const { error: profileError } = await supabase
          .from("profiles")
          .upsert({
            id: data.user.id,
            name: name.trim(),
            updated_at: new Date().toISOString()
          }, {
            onConflict: 'id'
          });

        if (profileError) {
          console.error("Error updating profile:", profileError);
          // Don't throw, just log - the trigger might have already created it
        }

        console.log("Navigating to profile page...");
        // Navigate to profile after successful signup
        // Check if we're in an iframe (Chrome extension context)
        const isInIframe = window.self !== window.top;
        
        if (isInIframe) {
          console.log("Detected iframe context, attempting navigation");
          try {
            // Try using postMessage to request navigation from parent (extension)
            if (window.parent && window.parent !== window.self) {
              window.parent.postMessage(
                { type: "NAVIGATE", path: "/profile" },
                "*" // In extension context, we can use wildcard
              );
              console.log("Navigation message sent to parent");
            }
            
            // Also try direct navigation as fallback
            setTimeout(() => {
              window.location.href = "/profile";
            }, 100);
          } catch (err) {
            console.error("Error navigating in iframe:", err);
            // Fallback to direct navigation
            window.location.href = "/profile";
          }
        } else {
          // Normal Next.js navigation
          setTimeout(() => {
            router.push("/profile");
            router.refresh();
          }, 100);
        }
      } else {
        console.error("No user data returned from sign up");
        throw new Error("No user data returned from sign up");
      }
    } catch (err: any) {
      console.error("Sign up error:", err);
      setError(err.message || "Failed to create account");
      setLoading(false);
    }
  };

  // Show loading state while checking authentication
  if (isCheckingAuth) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center px-6 py-12">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-6 py-12">
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -left-1/4 w-1/2 h-1/2 bg-white/[0.01] rounded-full blur-[120px]" />
        <div className="absolute bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-white/[0.01] rounded-full blur-[120px]" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md relative z-10"
      >
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
            <p className="text-neutral-400">Sign up to get started</p>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center gap-3"
            >
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
              <p className="text-sm text-red-400">{error}</p>
            </motion.div>
          )}

          <form 
            ref={formRef} 
            onSubmit={(e) => {
              e.preventDefault();
              e.stopPropagation();
              console.log("Form onSubmit triggered (should not happen with button type='button')");
            }} 
            className="space-y-6" 
            noValidate
          >
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-neutral-300 mb-2">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-neutral-300 mb-2">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-transparent"
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-neutral-300 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={6}
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-transparent"
                  placeholder="••••••••"
                />
              </div>
              <p className="mt-1 text-xs text-neutral-500">Must be at least 6 characters</p>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-neutral-300 mb-2">
                Confirm Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-transparent"
                  placeholder="••••••••"
                />
              </div>
              {password && confirmPassword && password === confirmPassword && (
                <p className="mt-1 text-xs text-green-400 flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" />
                  Passwords match
                </p>
              )}
            </div>

            <motion.button
              type="button"
              disabled={loading || isCheckingAuth}
              onClick={async (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                // Prevent any default navigation
                if (e.nativeEvent) {
                  e.nativeEvent.preventDefault();
                  e.nativeEvent.stopPropagation();
                  e.nativeEvent.stopImmediatePropagation();
                }
                
                console.log("=== BUTTON CLICKED ===", { 
                  loading, 
                  isCheckingAuth,
                  name, 
                  email,
                  passwordLength: password.length,
                  confirmPasswordLength: confirmPassword.length
                });
                
                if (loading || isCheckingAuth) {
                  console.log("Button disabled, returning early");
                  return;
                }
                
                // Manually create a form event and call the handler
                const syntheticEvent = {
                  preventDefault: () => {
                    console.log("preventDefault called");
                  },
                  stopPropagation: () => {
                    console.log("stopPropagation called");
                  },
                } as React.FormEvent<HTMLFormElement>;
                
                console.log("Calling handleSignUp...");
                await handleSignUp(syntheticEvent);
                console.log("handleSignUp completed");
              }}
              onMouseDown={(e) => {
                // Also prevent on mousedown to catch it early
                e.preventDefault();
                e.stopPropagation();
              }}
              whileHover={{ scale: loading ? 1 : 1.02 }}
              whileTap={{ scale: loading ? 1 : 0.98 }}
              className="w-full py-3 bg-white text-black rounded-lg font-semibold flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                "Creating account..."
              ) : (
                <>
                  Sign Up
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </motion.button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-neutral-400 text-sm">
              Already have an account?{" "}
              <Link href="/auth/signin" className="text-white hover:underline font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

