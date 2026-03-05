import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { LearningProgressModel } from "../models/learning-progress.model.js";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
export class LearningProgressRepository {
    filePath = path.join(__dirname, "../data/learning-progress.json");
    getAll() {
        const fileContent = fs.readFileSync(this.filePath, "utf-8");
        const data = JSON.parse(fileContent);
        return data.map((item) => LearningProgressModel.fromJSON(item));
    }
    saveAll(progress) {
        const data = progress.map((item) => item.toJSON());
        fs.writeFileSync(this.filePath, JSON.stringify(data, null, 2), "utf-8");
    }
    getByTheme(theme) {
        return this.getAll().filter((item) => item.theme === theme);
    }
    addOrUpdate(progress) {
        const allProgress = this.getAll();
        const existingIndex = allProgress.findIndex((item) => item.ticketId === progress.ticketId);
        if (existingIndex !== -1) {
            allProgress[existingIndex] = progress;
        }
        else {
            allProgress.push(progress);
        }
        this.saveAll(allProgress);
    }
    getNextId() {
        const allProgress = this.getAll();
        if (allProgress.length === 0) {
            return 1;
        }
        return Math.max(...allProgress.map((item) => item._id)) + 1;
    }
}
