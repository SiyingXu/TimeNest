window.assetsManifest = {
  version: 1,
  policy: {
    preferredFormats: ["avif", "webp", "png"],
    maxImageBytes: 1800000,
    maxSpriteBytes: 4200000,
    cache: {
      core: "precache",
      chapters: "runtime",
      cities: "runtime",
      cards: "runtime"
    }
  },
  core: [
    "assets/app-icon-pig-192.png",
    "assets/app-icon-pig-512.png",
    "assets/visual/card-pig-passport.svg",
    "assets/visual/generated/world-map-handdrawn.png",
    "assets/visual/generated/map-germany-route-handdrawn.png",
    "assets/visual/generated/map-germany-tuebingen-handdrawn.png",
    "assets/visual/generated/map-tuebingen-city-handdrawn.png",
    "assets/visual/generated/card-germany-cities-sprite.png",
    "assets/visual/generated/card-tuebingen-rewards-sprite.png",
    "assets/visual/generated/card-tuebingen-handdrawn.png",
    "assets/visual/generated/card-pig-passport-handdrawn.png"
  ],
  chapters: {
    "chapter-01": {
      name: "Germany route",
      preload: true,
      maps: ["assets/visual/generated/map-germany-route-handdrawn.png"],
      cities: [
        "tuebingen", "freiburg", "stuttgart", "heidelberg", "frankfurt", "cologne",
        "aachen", "bremen", "hamburg", "lubeck", "berlin", "dresden", "leipzig",
        "nuremberg", "rothenburg", "ulm", "munich", "fussen"
      ]
    },
    "chapter-02": {
      name: "Alpine route",
      preload: false,
      maps: ["assets/visual/generated/chapter-maps/chapter-02.png"],
      cities: []
    }
  },
  cityAssets: {
    tuebingen: {
      maps: ["assets/visual/generated/map-tuebingen-city-handdrawn.png"],
      cards: ["assets/visual/generated/card-tuebingen-rewards-sprite.png"]
    },
    freiburg: {
      maps: ["assets/visual/generated/map-freiburg-city-handdrawn.png"],
      cards: ["assets/visual/generated/card-freiburg-rewards-sprite.png"]
    }
  },
  futureLayout: {
    core: "assets/visual/generated/core/",
    chapters: "assets/visual/generated/chapters/chapter-XX/",
    cities: "assets/visual/generated/cities/<city-id>/",
    cards: "assets/visual/generated/cards/<city-id>/"
  }
};
