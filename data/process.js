const fs = require("fs");

try {
  const array = fs.readFileSync("git-class38.json", "utf-8");
  console.log(JSON.parse(array));
} catch {
  console.log("reading failed");
}
