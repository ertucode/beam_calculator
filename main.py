from beam_calculator import BeamCalculator

if __name__ == "__main__":
    b = BeamCalculator(10)
    b.load_from_json("samples/simply_supported_force_dist.json")
    b.mainloop()