from exam import Exam


class Information:
    _instance = None

    def __init__(self):
        self._exams = []
        self._records_count = 0
        self._scores_100_count = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.clear()

    @staticmethod
    def get_instance():
        if Information._instance is None:
            Information._instance = Information()

        return Information._instance

    @property
    def records_count(self):
        return self._records_count

    @property
    def scores_100_count(self):
        return self._scores_100_count

    def clear(self):
        self._records_count = 0
        self._scores_100_count = 0
        self._exams.clear()

    def load(self, ngroup, subject, lname, total_score_100, score, fname, total_score_5, patronymic, npass):
        try:
            exam = self.find(subject)
        except ValueError:
            exam = self.add(subject)

        exam.load(score, total_score_100, total_score_5, ngroup, lname, fname, patronymic, npass)

        self._records_count += 1
        if total_score_100 == 100:
            self._scores_100_count += 1

    def find(self, subject):
        index = self._exams.index(Exam(subject))
        exam = self._exams[index]
        return exam

    def add(self, subject):
        new_exam = Exam(subject)
        self._exams.append(new_exam)
        return new_exam

    def output(self, path, encoding="utf-8"):
        with open(path, "w", encoding=encoding) as out_file:
            self._output(out_file)

    def _output(self, file):
        result_data = self._get_subjects_list_with_max_mean()
        for info in result_data:
            file.write(f"{info['exam'].subject}\t{info['mean']:.1f}\t{info['count_of_failed']}\n")
            for student in info["less_than_95"]:
                file.write(f"\t{student.lname}\t{student.fname}\t{student.patronymic}\t{student.npass}\t{student.total_score_100}\t{student.total_score_5}\n")

    def _get_subjects_list_with_max_mean(self):
        result_data = []

        all_results = self._get_all_results()
        max_mean = self._get_max_mean(all_results)
        for info in all_results:
            if info["mean"] == max_mean:
                result_data.append(info)

        return result_data

    def _get_max_mean(self, all_results):
        max_mean = all_results[0]["mean"]

        for info in all_results:
            if info["mean"] > max_mean:
                max_mean = info["mean"]
        return max_mean

    def _get_all_results(self):
        res = []
        for exam in self._exams:
            info = {
                "exam": exam,
                "mean": self._get_exam_mean_score(exam),
                "count_of_failed": self._get_count_of_exam_failed(exam),
                "less_than_95": self._get_less_than_95(exam)
            }
            info["less_than_95"].sort(key=lambda x: x.npass)
            res.append(info)
        return res

    def _get_exam_mean_score(self, exam):
        sm = 0
        for student in exam:
            sm += student.total_score_100
        return sm / len(exam)

    def _get_count_of_exam_failed(self, exam):
        count = 0
        for student in exam:
            if student.total_score_5 < 3:
                count += 1
        return count

    def _get_less_than_95(self, exam):
        res = []
        for student in exam:
            if student.total_score_100 < 95:
                res.append(student)

        return res

