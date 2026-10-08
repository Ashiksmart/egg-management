export default function ComingSoon({ title, phase }: { title: string; phase: number }) {
  return (
    <div className="space-y-2">
      <h2 className="text-2xl font-bold">{title}</h2>
      <p className="text-stone-600">This screen will be built in Phase {phase}.</p>
    </div>
  );
}
