# Saved Catalog Sources

Saved October 22, 2026, Arizona time, for later catalog expansion and RAG source preparation.

## Catalog links

- [University of Arizona programs](https://catalog.arizona.edu/programs)
- [University of Arizona courses](https://catalog.arizona.edu/courses)

## Original CSV exports

The unchanged CSV files are in the team's [Catalog Sources folder](https://drive.google.com/drive/folders/1MASEtiCoBRITbGytE4wxbgEUFrDJMwZV).

| File | Subject | Course records |
| --- | --- | ---: |
| [courses-report.2026-10-23.csv](https://drive.google.com/file/d/1PnB6cBw7ljbb2hFfdVkoMm1coTfAMf0j/view?usp=drivesdk) | ECE | 186 |
| [courses-report.2026-10-23 (1).csv](https://drive.google.com/file/d/1AaZ4mNMHsJRlKJVlJtfItzmUwI51ZSPt/view?usp=drivesdk) | CSC | 114 |
| [courses-report.2026-10-23 (2).csv](https://drive.google.com/file/d/1k3trO-jurq9GE87pYVPk2evq7_U1PUiO/view?usp=drivesdk) | SFWE | 29 |
| Total | | 329 |

The filenames identify the exports as 2026-10-23. A catalog edition is not explicitly provided as a CSV column, so confirm it before assigning these records to an edition.

## Notes for the next implementation pass

- Preserve course IDs and catalog numbers as text, including leading zeros and suffixes.
- The files include descriptions, unit ranges, enrollment requirement fields, and course requisite fields.
- Enrollment requirement values can be internal reference IDs. Resolve their meaning before treating them as academic conditions.
- These are archived source inputs. The application's reviewed collection remains separate.
