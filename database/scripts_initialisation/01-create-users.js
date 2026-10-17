const database = db.getSiblingDB("ai_jobs");

const accounts = [
  {
    username: process.env.MONGO_APP_USERNAME,
    password: process.env.MONGO_APP_PASSWORD,
    role: "read",
  },
  {
    username: process.env.MONGO_IMPORT_USERNAME,
    password: process.env.MONGO_IMPORT_PASSWORD,
    role: "readWrite",
  },
];

// Vérifier toute la configuration avant de créer les comptes.
for (const account of accounts) {
  if (!account.username || !account.password) {
    throw new Error("Identifiant ou mot de passe manquant.");
  }
}

if (accounts[0].username === accounts[1].username) {
  throw new Error("Les deux comptes doivent avoir des noms distincts.");
}

for (const account of accounts) {
  if (database.getUser(account.username)) {
    print(`Compte déjà présent, inchangé : ${account.username}`);
    continue;
  }

  database.createUser({
    user: account.username,
    pwd: account.password,
    roles: [{ role: account.role, db: "ai_jobs" }],
  });

  print(`Compte créé : ${account.username} — rôle ${account.role}`);
}