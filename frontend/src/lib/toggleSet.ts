export class ToggleSet {
	private set: Set<string>;

	constructor() {
		this.set = new Set();
	}

	toggle(value: string) {
		if (this.set.has(value)) {
			this.set.delete(value);
		} else {
			this.set.add(value);
		}
	}

	has(value: string) {
		return this.set.has(value);
	}
}
