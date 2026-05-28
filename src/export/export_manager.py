import shutil
import pandas as pd

from pathlib import Path
from datetime import datetime


class ExportManager:

    def __init__(self, project_dir):

        self.project_dir = Path(project_dir)
        self.export_dir = self.project_dir / "exportacao_final"

        self.export_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def copy_outputs(self):

        folders = [
            "tables",
            "figures",
            "reports",
            "ecology",
            "machine_learning"
        ]

        for folder in folders:

            source = self.project_dir / folder

            if source.exists():

                destination = self.export_dir / folder

                if destination.exists():
                    shutil.rmtree(destination)

                shutil.copytree(source, destination)

    def create_summary_excel(self):

        excel_path = self.export_dir / "resumo_exportacao_athena.xlsx"

        summary = []

        for file in self.project_dir.rglob("*"):

            if file.is_file() and "exportacao_final" not in str(file):

                summary.append({
                    "arquivo": file.name,
                    "caminho": str(file),
                    "extensao": file.suffix,
                    "tamanho_kb": round(file.stat().st_size / 1024, 2)
                })

        df = pd.DataFrame(summary)

        df.to_excel(excel_path, index=False)

        return excel_path

    def create_zip(self):

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        zip_base = self.project_dir / f"ATHENA_EXPORT_{timestamp}"

        zip_path = shutil.make_archive(
            str(zip_base),
            "zip",
            self.export_dir
        )

        return zip_path

    def run(self):

        print("\n[ATHENA EXPORT] Preparando exportação final...")

        self.copy_outputs()

        summary_excel = self.create_summary_excel()

        zip_path = self.create_zip()

        print("[ATHENA EXPORT] Exportação concluída.")
        print(f"[ATHENA EXPORT] Excel resumo: {summary_excel}")
        print(f"[ATHENA EXPORT] Arquivo ZIP: {zip_path}")

        return {
            "export_dir": self.export_dir,
            "summary_excel": summary_excel,
            "zip_path": zip_path
        }
