## Date Filters 

## DateRangeFilter

Filter dates. It allows complex filter like:



| value                            | resulting filter                   | 
|----------------------------------|------------------------------------|
| 2000-01-01                       | equals 2000-01-01                  |
| =2000-01-01                      | equals 2000-01-01                  |
| > 2000-01-01                     | greater than 2000-01-03            |
| >= 2000-01-01                    | greater or equal than 2000-01-03   |
| < 2000-01-01                     | lower than 2000-01-03              |
| <= 2000-01-01                    | lower or equal than 2000-01-03     |
| 2000-01-02..2000-12-02           | between 2000-01-02 and  2000-12-02 |
| <> 2000-12-02                    | not equal to 2000-01-02            |
| 2000-01-01,2000-02-01,2000-03-01 | list of values                     |
