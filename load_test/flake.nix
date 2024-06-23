{
  description = "Empty Flake";
  nixConfig.bash-prompt = "[Empty] -> ";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: 
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        name = "Empty";
        buildInputs = with pkgs;[
          jmeter
      ];
    };
  };
}

