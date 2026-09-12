import { Bot, LoaderCircle, Send, Sparkles, User } from 'lucide-react';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import AgentResponse from '../components/AgentResponse';
import { askAgent } from '../services/agentService';

const exampleQuestions = ['Show dashboard summary', 'Forecast next 24 hours', 'Detect anomalies', 'Give recommendations'];

function AssistantPage() {
  const [messages, setMessages] = useState([{ id: 'welcome', role: 'assistant', content: 'Ask me about your energy dashboard, forecast, anomalies, recommendations, reports, or history.' }]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm({ defaultValues: { question: '' } });

  async function onSubmit({ question }) {
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || isLoading) return;
    setMessages((current) => [...current, { id: `${Date.now()}-user`, role: 'user', content: trimmedQuestion }]);
    setError(null);
    setIsLoading(true);
    reset();

    try {
      const response = await askAgent(trimmedQuestion);
      setMessages((current) => [...current, { id: `${Date.now()}-assistant`, role: 'assistant', response }]);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'The assistant could not process that request.');
    } finally {
      setIsLoading(false);
    }
  }

  function askExample(question) {
    setValue('question', question);
    handleSubmit(onSubmit)();
  }

  return (
    <section className="mx-auto flex min-h-[calc(100vh-72px)] w-full max-w-[1100px] flex-col px-5 py-8 sm:px-8">
      <div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-secondary">AI assistant</p><h1 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">Ask better questions about energy.</h1><p className="mt-2 text-sm text-slate-500">Your optimization copilot, connected to the live workspace services.</p></div>
      <div className="mt-8 flex-1 space-y-5 overflow-y-auto pb-6">
        {messages.map((message) => (
          <div key={message.id} className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {message.role === 'assistant' && <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-secondary/10 text-secondary"><Bot size={16} /></div>}
            {message.role === 'user' ? <div className="max-w-2xl rounded-2xl rounded-tr-md bg-primary px-4 py-3 text-sm text-white shadow-lg shadow-primary/10">{message.content}</div> : message.response ? <AgentResponse response={message.response} /> : <div className="max-w-2xl rounded-2xl rounded-tl-md border border-white/[0.07] bg-card px-4 py-3 text-sm leading-6 text-slate-400">{message.content}</div>}
            {message.role === 'user' && <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-white/[0.06] text-slate-400"><User size={16} /></div>}
          </div>
        ))}
        {isLoading && <div className="flex items-center gap-3"><div className="flex h-8 w-8 items-center justify-center rounded-xl bg-secondary/10 text-secondary"><Bot size={16} /></div><div className="flex items-center gap-1 rounded-2xl rounded-tl-md border border-white/[0.07] bg-card px-4 py-4"><span className="h-1.5 w-1.5 animate-bounce rounded-full bg-secondary [animation-delay:-0.3s]" /><span className="h-1.5 w-1.5 animate-bounce rounded-full bg-secondary [animation-delay:-0.15s]" /><span className="h-1.5 w-1.5 animate-bounce rounded-full bg-secondary" /></div></div>}
        {error && <p className="ml-11 text-xs text-red-300">{error}</p>}
      </div>
      <div className="border-t border-white/[0.06] pt-5">
        <div className="mb-3 flex flex-wrap gap-2">{exampleQuestions.map((question) => <button key={question} type="button" onClick={() => askExample(question)} disabled={isLoading} className="flex items-center gap-1.5 rounded-full border border-white/[0.08] px-3 py-1.5 text-xs text-slate-400 transition hover:border-secondary/30 hover:text-secondary disabled:cursor-not-allowed disabled:opacity-50"><Sparkles size={12} />{question}</button>)}</div>
        <form onSubmit={handleSubmit(onSubmit)} className="flex items-end gap-2 rounded-2xl border border-white/[0.08] bg-card p-2 focus-within:border-primary/40"><textarea {...register('question', { required: 'Ask a question to continue.' })} rows={1} disabled={isLoading} placeholder="Ask about your energy data..." className="max-h-28 min-h-10 flex-1 resize-none bg-transparent px-3 py-2.5 text-sm text-white outline-none placeholder:text-slate-600 disabled:opacity-50" onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); handleSubmit(onSubmit)(); } }} /><button type="submit" aria-label="Send question" disabled={isLoading} className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50">{isLoading ? <LoaderCircle size={17} className="animate-spin" /> : <Send size={17} />}</button></form>
        {errors.question && <p className="mt-2 text-xs text-red-300">{errors.question.message}</p>}
      </div>
    </section>
  );
}

export default AssistantPage;
