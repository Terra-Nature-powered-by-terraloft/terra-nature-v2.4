import { Navigation } from '@/components/landing/Navigation';
import { Hero } from '@/components/landing/Hero';
import { Features } from '@/components/landing/Features';
import { Stats } from '@/components/landing/Stats';
import { Gallery } from '@/components/landing/Gallery';
import { Team } from '@/components/landing/Team';
import { CTA } from '@/components/landing/CTA';
import { Footer } from '@/components/landing/Footer';

export default function Home() {
  return (
    <>
      <Navigation />
      <main>
        <Hero />
        <Features />
        <Stats />
        <Gallery />
        <Team />
        <CTA />
      </main>
      <Footer />
    </>
  );
}
