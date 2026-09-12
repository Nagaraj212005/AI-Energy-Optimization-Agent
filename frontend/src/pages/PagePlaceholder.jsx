function PagePlaceholder({ eyebrow, title, description }) {
  return (
    <section className="mx-auto flex min-h-[calc(100vh-72px)] w-full max-w-[1400px] items-center justify-center px-5 py-8 sm:px-8">
      <div className="max-w-lg text-center">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-secondary">{eyebrow}</p>
        <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">{title}</h1>
        <p className="mt-4 text-sm leading-6 text-slate-500">{description}</p>
      </div>
    </section>
  );
}

export default PagePlaceholder;
