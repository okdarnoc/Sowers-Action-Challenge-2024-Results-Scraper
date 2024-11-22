# Sowers Action Challenge 2024 Results Scraper

A Python script specifically designed to collect race timing data from the 12 Hours Sowers Action Challenge 2024. Since the official platform only allows individual result lookups without providing a comprehensive ranking table, this tool helps compile complete race statistics.

## Purpose

The Sowers Action Challenge 2024 timing platform (IBanSport) only allows participants to check individual results using bib numbers. This makes it difficult to:
- See overall race standings
- Compare performance across checkpoints
- Analyze race progression
- Track friends and team members

This script addresses these limitations by collecting all available race data into a single CSV file for analysis.

## Features

- Collects all runner data from the 12 Hours Sowers Action Challenge 2024:
  - Bib number
  - Runner name
  - Category ranking
  - All checkpoint times (CP1-CP5)
  - Finish times
- Processes the entire bib number range of the event
- Creates automatic backups to prevent data loss
- Supports interrupted scraping resumption
- Timestamps all entries for tracking data freshness

## Prerequisites

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sowers-action-scraper.git
cd sowers-action-scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python race_scraper.py
```

The script will automatically:
- Create a backup if previous results exist
- Skip already processed bib numbers
- Handle connection issues gracefully
- Save results progressively

## Output Format

The script generates `race_results.csv` with the following structure:
```
Bib Number, Runner Name, Category Ranking, CP1 Time, CP2 Time, CP3 Time, CP4 Time, CP5 Time, FP Time, Timestamp
1001, John Doe, Overall: 45, 01:23:45, 02:45:12, 04:01:23, 05:30:45, 07:15:33, 08:45:22, 2024-02-24 15:30:45
```

## Data Analysis Possibilities

With the compiled data, you can:
- Generate complete race rankings
- Calculate checkpoint split times
- Analyze pacing strategies
- Compare performance across categories
- Track team/group performance
- Create custom race reports

## Ethical Considerations

- This script only collects publicly available data that any participant can access
- Uses reasonable delays between requests to not overload the timing server
- Recommended to run during off-peak hours
- Data should be used responsibly and in accordance with race organizer guidelines

## Rate Limiting

The script includes configurable delays between requests to be respectful to the server:
- Default delay: 0 seconds (adjustable in code)
- Error delay: 5 seconds
- Adjust these values based on server response and load

## Limitations

- Only collects data that is publicly available via the IBanSport platform
- Accuracy depends on the timing system's data updates
- May need adjustment if bib number ranges change
- Network connectivity affects completion time

## Contributing

Contributions to improve the script are welcome:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for information gathering purposes only. Users should:
- Respect the race organizer's systems and policies
- Use the data responsibly
- Not use the collected data for commercial purposes
- Be aware that race results are preliminary until officially confirmed

## Author

Your Name
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## Acknowledgments

- Sowers Action Challenge organizers for hosting the event
- IBanSport for providing the timing platform
- All participants who make this event possible