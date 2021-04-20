from student import Student


class Information:
	_instance = None

	def __init__(self):
		self._students = []
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
		self._students.clear()

	def load(self, npass, ngroup, fname, lname, patronymic, subject, score, total_score_100, total_score_5):
		try:
			student = self.find(npass)
		except ValueError:
			student = self.add(npass, ngroup, fname, lname, patronymic)

		if student.ngroup != ngroup:
			raise ValueError

		student.load(subject, score, total_score_100, total_score_5)

		self._records_count += 1
		if total_score_100 == 100:
			self._scores_100_count += 1

	def add(self, npass, ngroup, fname, lname, patronymic) -> Student:
		new_student = Student(npass, ngroup, fname, lname, patronymic)
		self._students.append(new_student)
		self._records_count += 1
		return new_student

	def find(self, npass) -> Student:
		index = self._students.index(Student(npass))
		student = self._students[index]
		return student

	def output(self, path, encoding="utf-8"):
		with open(path, "w", encoding=encoding) as out_file:
			self._output(out_file)



	def _output(self, file):
		self._students.sort(key=lambda stud: stud.npass)

		result_data = self._get_resulted_dict()

		print(result_data)
		pass

	def _get_resulted_dict(self):
		result_data = dict()

		for student in self._students:
			for exam in student:
				if result_data.get(exam.subject) is None:
					result_data[exam.subject] = {"mean": None, "students": [], "exams": []}

				result_data[exam.subject]["students"].append(student)
				result_data[exam.subject]["exams"].append(exam)

		for info in result_data.values():
			sum_scores = sum(exam.total_score_5 for exam in info["exams"])
			info["mean"] = sum_scores / len(info["exams"])

		return result_data



if __name__ == "__main__":
	from builder import Builder
	storage = Information.get_instance()
	with open("data.csv", "r") as f:
		builder = Builder()
		builder.load(Information.get_instance(), f)

	storage._students.sort(key=lambda stud: stud.npass)

	for st in storage._students:
		print(st)


	print()
	print()
	print()
	print( storage._get_resulted_dict() )




