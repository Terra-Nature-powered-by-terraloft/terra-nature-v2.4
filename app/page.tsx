import { Navigation } from '@/components/landing/Navigation';
import { Hero } from '@/components/landing/Hero';
import { ProblemSolution } from '@/components/landing/ProblemSolution';
import { Features } from '@/components/landing/Features';
import { BrandPillars } from '@/components/landing/BrandPillars';
import { Stats } from '@/components/landing/Stats';
import { ProcessFlow } from '@/components/landing/ProcessFlow';
import { Team } from '@/components/landing/Team';
import { UseCases } from '@/components/landing/UseCases';
import { DashboardPreview } from '@/components/landing/DashboardPreview';
import { CTA } from '@/components/landing/CTA';
import { Footer } from '@/components/landing/Footer';

export default function Home() {
  return (
    <>
      <Navigation />
      <main>
        <Hero />
        <ProblemSolution />
        <Features />
        <BrandPillars />
        <Stats />
        <ProcessFlow />
        <Team />
        <UseCases />
        <DashboardPreview />
        <CTA />
      </main>
      <Footer />
    </>
  );
}
