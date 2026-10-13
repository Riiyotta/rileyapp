// §4.1 cards and §4.2 modal content (text from the saved page's Storyblok payload).
// `curious` and `friendly` icons are broken on the live site (§16) — icon: null renders no image.
export const MASCOTS = {
  worrier: {
    svg: '/assets/modal/mascots/worrier.svg',
    gradient: 'bg-[radial-gradient(58.33%_52.53%_at_50%_50%,#D7BEFC_0%,#FFF_100%)]',
  },
  guide: {
    svg: '/assets/modal/mascots/guide.svg',
    gradient: 'bg-[radial-gradient(64.92%_39.36%_at_50.04%_52.53%,#4598E6_0%,#FFF_100%)]',
  },
  softie: {
    svg: '/assets/modal/mascots/softie.svg',
    gradient: 'bg-[radial-gradient(64.92%_39.36%_at_50.04%_52.53%,#62D09E_0%,#FFF_100%)]',
  },
  spark: {
    svg: '/assets/modal/mascots/spark.svg',
    gradient: 'bg-[radial-gradient(58.33%_52.53%_at_50%_50%,#E8899E_0%,#FFF_100%)]',
  },
  uplifter: {
    svg: '/assets/modal/mascots/uplifter.svg',
    gradient: 'bg-[radial-gradient(58.33%_52.53%_at_50%_50%,#FFA552_0%,#FFF_100%)]',
  },
  explorer: {
    svg: '/assets/modal/mascots/explorer.svg',
    gradient: 'bg-[radial-gradient(58.33%_52.53%_at_50%_50%,#FFD55D_0%,#FFF_100%)]',
  },
}

export const SUPERPOWERS = [
  {
    icon: '/assets/bottle.svg',
    text: 'Survive the newborn stage',
    modal: {
      mascot: 'worrier',
      title: 'Lost in the newborn phase fog?',
      subtitle: 'You’re not alone. Riley can:',
      features: [
        { icon: 'puzzle', title: 'Get advice just for you', description: "Riley takes pediatrician-vetted advice and applies it to your family's unique situation." },
        { icon: 'ruler', title: 'Keep track of everything', description: 'Easily track sleep, feedings, whatever, in the only app where your data is put to work.' },
        { icon: 'handsTogether', title: 'Provide 24/7 support', description: 'Expert-backed support all day and night for all those “is this normal?” moments.' },
        { icon: 'lightbulb', title: 'Predict naps and feeds', description: "Riley's Golden Window™ helps you take the guesswork out of sleep and feeding." },
      ],
    },
  },
  {
    icon: '/assets/moon.svg',
    text: 'Get help with naps and sleep',
    modal: {
      mascot: 'guide',
      title: 'Tired of playing the nap guessing game?',
      subtitle: 'We’ve been there! Riley can:',
      features: [
        { icon: 'lightbulb', title: 'Take the guesswork out', description: "Predict your baby's ideal naptime and bedtime with Riley's Golden Window™." },
        { icon: 'knight', title: 'Solve regressions, fast', description: 'Riley helps you handle regressions with expert-backed support.' },
        { icon: 'ladder', title: 'Real-time adjustments', description: 'Riley learns your baby’s patterns and adjusts your support in real-time.' },
        { icon: 'affectionate', title: 'Personalize routines', description: 'Create calm sleep routines that work for your family, now and in the long-term.' },
      ],
    },
  },
  {
    icon: '/assets/blocks.svg',
    text: 'Support baby development',
    modal: {
      mascot: 'softie',
      title: 'Worried about milestones?',
      subtitle: "Yup, we've been there. Riley can:",
      features: [
        { icon: 'ruler', title: 'Track milestones', description: 'Track key milestones and prep you for what’s next for your little one.' },
        { icon: null, title: 'Help plan activities', description: 'Riley suggests age-appropriate, science-backed activities vetted by pediatricians.' },
        { icon: 'music', title: 'Guide development', description: 'Riley helps spot patterns and trends to help guide healthy development.' },
        { icon: 'independent', title: 'No comparisons', description: 'Riley gives personalized, data-driven support. No one-size-fits-all advice here.' },
      ],
    },
  },
  {
    icon: '/assets/stubborn.svg',
    text: 'Navigating toddler tantrums',
    modal: {
      mascot: 'spark',
      title: 'Tantrums testing your patience?',
      subtitle: 'You’re not alone! Riley can:',
      features: [
        { icon: null, title: 'Decode the why', description: 'Riley learns from what you’ve shared to help navigate meltdowns.' },
        { icon: null, title: 'Match your needs', description: 'Riley suggests calming techniques that match your individual child’s needs.' },
        { icon: 'books', title: 'Learn from what works', description: "Riley helps track behaviors to spot what works - and what doesn't! - for your family." },
        { icon: 'heartParachute', title: 'Sanity reminders', description: 'Riley understands the science behind big toddler feelings - and guides you through it.' },
      ],
    },
  },
  {
    icon: '/assets/bowl.svg',
    text: 'Starting solid foods',
    modal: {
      mascot: 'uplifter',
      title: 'Not sure how to start solids?',
      subtitle: 'We know how that feels. Riley can:',
      features: [
        { icon: 'octopus', title: 'Guide you through it', description: 'Riley walks you through the what, when, and how of feeding.' },
        { icon: 'everything', title: 'Personalized meal tips', description: 'Get meal tips based on your actual baby’s current routine.' },
        { icon: 'ruler', title: 'Track feedings', description: 'Riley helps you keep track of different foods, reactions, and preferences.' },
        { icon: 'heartParachute', title: 'Take the pressure off', description: 'Riley makes starting solids simpler, so you can focus on the joy, not the stress.' },
      ],
    },
  },
  {
    icon: '/assets/sailboat.svg',
    text: 'Build a routine',
    modal: {
      mascot: 'explorer',
      title: 'Feeling like every day is chaos?',
      subtitle: "It's totally normal! Riley can:",
      features: [
        { icon: 'calendar', title: 'Personalize routines', description: 'Riley creates a routine around your baby’s actual sleep and feed patterns.' },
        { icon: 'magicWand', title: 'Grow with you', description: 'Needs change quickly with littles! Riley is the only app that grows with your family.' },
        { icon: 'rocket', title: 'Proactively advise', description: 'Riley suggests age-appropriate activities based on your real-time data.' },
        { icon: 'elephant', title: 'Take the guesswork out', description: 'Get expert, pediatrician-backed advice for every “What now?” moment.' },
      ],
    },
  },
]
