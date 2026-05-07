"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const INSTRUMENTS = ["General", "Piano", "Guitar", "Voice", "Other"];

type Session = {
  id: number;
  created_at: string;
  tempo_bpm: number | null;
  pitch_hz: number | null;
  dynamic_rms: number | null;
  feedback: string | null;
};

export default function Dashboard() {
  const router = useRouter();
  const fileRef = useRef<HTMLInputElement>(null);

  const [token, setToken] = useState<string | null>(null);
  const [instrument, setInstrument] = useState("General");
  const [uploading, setUploading] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selected, setSelected] = useState<Session | null>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (!session) {
        router.replace("/");
      } else {
        setToken(session.access_token);
        fetchSessions(session.access_token);
      }
    });
  }, [router]);

  async function fetchSessions(accessToken: string) {
    const res = await fetch(`${API_URL}/sessions`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (res.ok) setSessions(await res.json());
  }

  async function handleUpload(e: { preventDefault: () => void }) {
    e.preventDefault();
    const file = fileRef.current?.files?.[0];
    if (!file || !token) return;

    setUploading(true);
    setError("");
    setFeedback(null);
    setSelected(null);

    const form = new FormData();
    form.append("audio", file);
    form.append("instrument", instrument);

    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: form,
    });

    if (res.ok) {
      const data = await res.json();
      setFeedback(data.feedback);
      fetchSessions(token);
    } else {
      setError("Analysis failed. Make sure the file is a valid audio recording.");
    }
    setUploading(false);
  }

  async function handleSignOut() {
    await supabase.auth.signOut();
    router.replace("/");
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <header className="flex items-center justify-between px-6 py-4 border-b border-zinc-800">
        <span className="font-bold text-lg">Maestro</span>
        <button
          onClick={handleSignOut}
          className="text-sm text-zinc-400 hover:text-white transition-colors"
        >
          Sign out
        </button>
      </header>

      <div className="max-w-3xl mx-auto px-6 py-10 flex flex-col gap-10">
        {/* Upload */}
        <section>
          <h2 className="text-lg font-semibold mb-4">New session</h2>
          <form onSubmit={handleUpload} className="flex flex-col gap-4">
            <div className="flex gap-3">
              <input
                ref={fileRef}
                type="file"
                accept="audio/*"
                required
                className="flex-1 rounded-lg bg-zinc-800 border border-zinc-700 px-4 py-2.5 text-sm text-zinc-300 file:mr-3 file:rounded file:border-0 file:bg-zinc-700 file:px-3 file:py-1 file:text-xs file:text-zinc-200 focus:outline-none"
              />
              <select
                value={instrument}
                onChange={(e) => setInstrument(e.target.value)}
                className="rounded-lg bg-zinc-800 border border-zinc-700 px-3 py-2.5 text-sm text-zinc-300 focus:outline-none"
              >
                {INSTRUMENTS.map((i) => (
                  <option key={i}>{i}</option>
                ))}
              </select>
            </div>
            {error && <p className="text-red-400 text-xs">{error}</p>}
            <button
              type="submit"
              disabled={uploading}
              className="self-start rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 px-5 py-2.5 text-sm font-semibold transition-colors"
            >
              {uploading ? "Analyzing…" : "Analyze recording"}
            </button>
          </form>
        </section>

        {/* Feedback */}
        {feedback && (
          <section>
            <h2 className="text-lg font-semibold mb-3">Feedback</h2>
            <div className="rounded-xl bg-zinc-900 border border-zinc-800 px-6 py-5 text-sm text-zinc-300 whitespace-pre-wrap leading-relaxed">
              {feedback}
            </div>
          </section>
        )}

        {/* History */}
        {sessions.length > 0 && (
          <section>
            <h2 className="text-lg font-semibold mb-3">Past sessions</h2>
            <ul className="flex flex-col gap-2">
              {sessions.map((s) => (
                <li key={s.id}>
                  <button
                    onClick={() => setSelected(selected?.id === s.id ? null : s)}
                    className="w-full text-left rounded-xl bg-zinc-900 border border-zinc-800 hover:border-zinc-600 px-5 py-4 transition-colors"
                  >
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-zinc-300">
                        {new Date(s.created_at).toLocaleDateString(undefined, {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </span>
                      <span className="text-zinc-500 text-xs">
                        {s.tempo_bpm ? `${Math.round(s.tempo_bpm)} BPM` : ""}
                        {s.dynamic_rms ? ` · RMS ${s.dynamic_rms.toFixed(3)}` : ""}
                      </span>
                    </div>
                    {selected?.id === s.id && s.feedback && (
                      <p className="mt-3 text-xs text-zinc-400 whitespace-pre-wrap leading-relaxed">
                        {s.feedback}
                      </p>
                    )}
                  </button>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </main>
  );
}
